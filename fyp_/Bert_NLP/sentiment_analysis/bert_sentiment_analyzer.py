# -*- coding: utf-8 -*-



import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import json
import csv
import os

import bert
from bert import run_classifier
from tqdm import tqdm

MAX_SEQ_LENGTH = 128
BATCH_SIZE = 32
LEARNING_RATE = 2e-5
NUM_TRAIN_EPOCHS = 3.0
WARMUP_PROPORTION = 0.1
SAVE_CHECKPOINTS_STEPS = 500
SAVE_SUMMARY_STEPS = 100
DATA_COLUMN = 7
LABEL_COLUMN = 0
label_list = [0, 1]

num_train_steps = 18000 # Corresponding to the model.ckpt-**** number at OUTPUT_DIR
num_warmup_steps = int(num_train_steps * WARMUP_PROPORTION)

#OUTPUT_DIR = r"..\fine_tuning\bert_model"
OUTPUT_DIR = r"C:\Users\Lawrann\Google Drive\bert_model"

# This is a path to an uncased (all lowercase) version of BERT
BERT_MODEL_HUB = "https://tfhub.dev/google/bert_uncased_L-12_H-768_A-12/1"

#%%
def create_tokenizer_from_hub_module():
  """Get the vocab file and casing info from the Hub module."""
  with tf.Graph().as_default():
    bert_module = hub.Module(BERT_MODEL_HUB)
    tokenization_info = bert_module(signature="tokenization_info", as_dict=True)
    with tf.Session() as sess:
      vocab_file, do_lower_case = sess.run([tokenization_info["vocab_file"],
                                            tokenization_info["do_lower_case"]])
      
  return bert.tokenization.FullTokenizer(
      vocab_file=vocab_file, do_lower_case=do_lower_case)

tokenizer = create_tokenizer_from_hub_module()


#%%
def create_model(is_predicting, input_ids, input_mask, segment_ids, labels,
                 num_labels):
  """Creates a classification model."""

  bert_module = hub.Module(
      BERT_MODEL_HUB,
      trainable=True)
  bert_inputs = dict(
      input_ids=input_ids,
      input_mask=input_mask,
      segment_ids=segment_ids)
  bert_outputs = bert_module(
      inputs=bert_inputs,
      signature="tokens",
      as_dict=True)

  # Use "pooled_output" for classification tasks on an entire sentence.
  # Use "sequence_outputs" for token-level output.
  output_layer = bert_outputs["pooled_output"]

  hidden_size = output_layer.shape[-1].value

  # Create our own layer to tune for politeness data.
  output_weights = tf.get_variable(
      "output_weights", [num_labels, hidden_size],
      initializer=tf.truncated_normal_initializer(stddev=0.02))

  output_bias = tf.get_variable(
      "output_bias", [num_labels], initializer=tf.zeros_initializer())

  with tf.variable_scope("loss"):

    # Dropout helps prevent overfitting
    output_layer = tf.nn.dropout(output_layer, keep_prob=0.9)

    logits = tf.matmul(output_layer, output_weights, transpose_b=True)
    logits = tf.nn.bias_add(logits, output_bias)
    log_probs = tf.nn.log_softmax(logits, axis=-1)

    # Convert labels into one-hot encoding
    one_hot_labels = tf.one_hot(labels, depth=num_labels, dtype=tf.float32)

    predicted_labels = tf.squeeze(tf.argmax(log_probs, axis=-1, output_type=tf.int32))
    # If we're predicting, we want predicted labels and the probabiltiies.
    if is_predicting:
      return (predicted_labels, log_probs)

    # If we're train/eval, compute loss between predicted and actual label
    per_example_loss = -tf.reduce_sum(one_hot_labels * log_probs, axis=-1)
    loss = tf.reduce_mean(per_example_loss)
    return (loss, predicted_labels, log_probs)

# model_fn_builder actually creates our model function
# using the passed parameters for num_labels, learning_rate, etc.
def model_fn_builder(num_labels, learning_rate, num_train_steps,
                     num_warmup_steps):
  """Returns `model_fn` closure for TPUEstimator."""
  def model_fn(features, labels, mode, params):  # pylint: disable=unused-argument
    """The `model_fn` for TPUEstimator."""

    input_ids = features["input_ids"]
    input_mask = features["input_mask"]
    segment_ids = features["segment_ids"]
    label_ids = features["label_ids"]

    is_predicting = (mode == tf.estimator.ModeKeys.PREDICT)
    
    # TRAIN and EVAL
    if not is_predicting:

      (loss, predicted_labels, log_probs) = create_model(
        is_predicting, input_ids, input_mask, segment_ids, label_ids, num_labels)

      train_op = bert.optimization.create_optimizer(
          loss, learning_rate, num_train_steps, num_warmup_steps, use_tpu=False)

      # Calculate evaluation metrics. 
      def metric_fn(label_ids, predicted_labels):
        accuracy = tf.metrics.accuracy(label_ids, predicted_labels)
        f1_score = tf.contrib.metrics.f1_score(
            label_ids,
            predicted_labels)
        auc = tf.metrics.auc(
            label_ids,
            predicted_labels)
        recall = tf.metrics.recall(
            label_ids,
            predicted_labels)
        precision = tf.metrics.precision(
            label_ids,
            predicted_labels) 
        true_pos = tf.metrics.true_positives(
            label_ids,
            predicted_labels)
        true_neg = tf.metrics.true_negatives(
            label_ids,
            predicted_labels)   
        false_pos = tf.metrics.false_positives(
            label_ids,
            predicted_labels)  
        false_neg = tf.metrics.false_negatives(
            label_ids,
            predicted_labels)
        return {
            "eval_accuracy": accuracy,
            "f1_score": f1_score,
            "auc": auc,
            "precision": precision,
            "recall": recall,
            "true_positives": true_pos,
            "true_negatives": true_neg,
            "false_positives": false_pos,
            "false_negatives": false_neg
        }

      eval_metrics = metric_fn(label_ids, predicted_labels)

      if mode == tf.estimator.ModeKeys.TRAIN:
        return tf.estimator.EstimatorSpec(mode=mode,
          loss=loss,
          train_op=train_op)
      else:
          return tf.estimator.EstimatorSpec(mode=mode,
            loss=loss,
            eval_metric_ops=eval_metrics)
    else:
      (predicted_labels, log_probs) = create_model(
        is_predicting, input_ids, input_mask, segment_ids, label_ids, num_labels)

      predictions = {
          'probabilities': log_probs,
          'labels': predicted_labels
      }
      return tf.estimator.EstimatorSpec(mode, predictions=predictions)

  # Return the actual model function in the closure
  return model_fn

#%%1
run_config = tf.estimator.RunConfig(
    model_dir=OUTPUT_DIR,
    save_summary_steps=SAVE_SUMMARY_STEPS,
    save_checkpoints_steps=SAVE_CHECKPOINTS_STEPS)
model_fn = model_fn_builder(
  num_labels=len(label_list),
  learning_rate=LEARNING_RATE,
  num_train_steps=num_train_steps,
  num_warmup_steps=num_warmup_steps)

estimator = tf.estimator.Estimator(
  model_fn=model_fn,
  config=run_config,
  params={"batch_size": BATCH_SIZE})

#%%
def getPrediction(in_sentences):
  labels = ["-1", "1"]
  input_examples = [run_classifier.InputExample(guid="", text_a = x, text_b = None, label = 0) for x in in_sentences] # here, "" is just a dummy label
  print("HERE1")
  input_features = run_classifier.convert_examples_to_features(input_examples, label_list, MAX_SEQ_LENGTH, tokenizer)
  print("HERE2")
  predict_input_fn = run_classifier.input_fn_builder(features=input_features, seq_length=MAX_SEQ_LENGTH, is_training=False, drop_remainder=False)
  print("HERE3")
  predictions = estimator.predict(predict_input_fn)
  print("HERE4")
  print(predictions)
#  predictions = estimator.predict(input_fn=predict_input_fn, yield_single_examples=False)
  return [(sentence, prediction['probabilities'], labels[prediction['labels']]) for sentence, prediction in zip(in_sentences, predictions)]

#%%
  
# For news articles
articles_path = r"..\..\Articles\articles_cleaned"

#%%
#SP
if not os.path.exists('sentimentdata\sp_articles_sentiment_csv'):
    os.makedirs('sentimentdata\sp_articles_sentiment_csv')
if not os.path.exists('sentimentdata\sp_articles_sentiment_json'):
    os.makedirs('sentimentdata\sp_articles_sentiment_json')
    
abstract_list = []
headline_list = []
snippet_list = []
lead_paragraph_list = []
filter_tweet_list = []

with open(articles_path+r'\sp_articles\sp_articles_cleaned.json') as json_file:
    data = json.load(json_file)
    for i in data:
        abstract_list.append(i['abstract'])
        headline_list.append(i['headline'])
        snippet_list.append(i['snippet'])
        lead_paragraph_list.append(i['lead_paragraph'])
        
    abstract_sentiment = getPrediction(abstract_list)
    headline_sentiment = getPrediction(headline_list)
    snippet_sentiment = getPrediction(snippet_list)
    lead_paragraph_sentiment = getPrediction(lead_paragraph_list)
        
    for i in tqdm(range(len(data))):
        dic = {}
        dic['date'] = str(data[i]['date'])
        dic['abstract'] = str(data[i]['abstract'])
        dic['headline'] = str(data[i]['headline'])
        dic['snippet'] = str(data[i]['snippet'])
        dic['lead_paragraph'] = str(data[i]['lead_paragraph'])
        dic['abstract_sentiment'] = str(abstract_sentiment[i][2])
        dic['headline_sentiment'] = str(headline_sentiment[i][2])
        dic['snippet_sentiment'] = str(snippet_sentiment[i][2])
        dic['lead_paragraph_sentiment'] = str(lead_paragraph_sentiment[i][2])
        
        sentiment_sum = int(abstract_sentiment[i][2]) + int(headline_sentiment[i][2]) + int(snippet_sentiment[i][2]) + int(lead_paragraph_sentiment[i][2])
        if (int(sentiment_sum) == 0):
            dic['sentiment'] = '0'
        elif (int(sentiment_sum) > 0):
            dic['sentiment'] = '1'
        elif (int(sentiment_sum) < 0):
            dic['sentiment'] = '-1'
        filter_tweet_list.append(dic)
        
with open('sentimentdata\sp_articles_sentiment_csv\sp_articles_sentiment.csv', 'w', newline='', encoding='utf-8') as output_file:
    keys = filter_tweet_list[0].keys()   
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(filter_tweet_list)

with open('sentimentdata\sp_articles_sentiment_json\sp_articles_sentiment.json', 'w') as fp:
    json.dump(filter_tweet_list, fp)

#%%
#Citi
if not os.path.exists('sentimentdata\citi_articles_sentiment_csv'):
    os.makedirs('sentimentdata\citi_articles_sentiment_csv')
if not os.path.exists('sentimentdata\citi_articles_sentiment_json'):
    os.makedirs('sentimentdata\citi_articles_sentiment_json')
    
abstract_list = []
headline_list = []
snippet_list = []
lead_paragraph_list = []
filter_tweet_list = []

with open(articles_path+r'\citi_articles\citi_articles_cleaned.json') as json_file:
    data = json.load(json_file)
    for i in data:
        abstract_list.append(i['abstract'])
        headline_list.append(i['headline'])
        snippet_list.append(i['snippet'])
        lead_paragraph_list.append(i['lead_paragraph'])
        
    abstract_sentiment = getPrediction(abstract_list)
    headline_sentiment = getPrediction(headline_list)
    snippet_sentiment = getPrediction(snippet_list)
    lead_paragraph_sentiment = getPrediction(lead_paragraph_list)
        
    for i in tqdm(range(len(data))):
        dic = {}
        dic['date'] = str(data[i]['date'])
        dic['abstract'] = str(data[i]['abstract'])
        dic['headline'] = str(data[i]['headline'])
        dic['snippet'] = str(data[i]['snippet'])
        dic['lead_paragraph'] = str(data[i]['lead_paragraph'])
        dic['abstract_sentiment'] = str(abstract_sentiment[i][2])
        dic['headline_sentiment'] = str(headline_sentiment[i][2])
        dic['snippet_sentiment'] = str(snippet_sentiment[i][2])
        dic['lead_paragraph_sentiment'] = str(lead_paragraph_sentiment[i][2])
        
        sentiment_sum = int(abstract_sentiment[i][2]) + int(headline_sentiment[i][2]) + int(snippet_sentiment[i][2]) + int(lead_paragraph_sentiment[i][2])
        if (int(sentiment_sum) == 0):
            dic['sentiment'] = '0'
        elif (int(sentiment_sum) > 0):
            dic['sentiment'] = '1'
        elif (int(sentiment_sum) < 0):
            dic['sentiment'] = '-1'
        filter_tweet_list.append(dic)
        
with open('sentimentdata\citi_articles_sentiment_csv\citi_articles_sentiment.csv', 'w', newline='', encoding='utf-8') as output_file:
    keys = filter_tweet_list[0].keys()   
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(filter_tweet_list)

with open('sentimentdata\citi_articles_sentiment_json\citi_articles_sentiment.json', 'w') as fp:
    json.dump(filter_tweet_list, fp)


#%%
#For tweets
month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
year = ['14','15','16','17','18']
tweets_path = "..\..\Tweets\clean3"

#%%
#CITI
if not os.path.exists('sentimentdata\citi_tweets_sentiment_csv'):
    os.makedirs('sentimentdata\citi_tweets_sentiment_csv')
if not os.path.exists('sentimentdata\citi_tweets_sentiment_json'):
    os.makedirs('sentimentdata\citi_tweets_sentiment_json')

for yr in year:
    for mth in tqdm(month):
        filter_tweet_list = []
        text_list = []
        with open(tweets_path+'\citicleanjson\citi_tweets_removeduplicates_'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            for i in data:
                text_list.append(i[2])
            sentiment = getPrediction(text_list)
            for i in tqdm(range(len(data))):
                dic = {}
                dic['username'] = str(data[i][0])
                dic['date'] = str(data[i][1])
                dic['text'] = str(data[i][2])
                dic['sentiment'] = str(sentiment[i][2])
                dic['confidence_1'] = str(sentiment[i][1][0])
                dic['confidence_2'] = str(sentiment[i][1][1])
                filter_tweet_list.append(dic)
                
        keys = filter_tweet_list[0].keys()        
        with open('sentimentdata\citi_tweets_sentiment_csv\citi_test'+yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(filter_tweet_list)
        
        with open('sentimentdata\citi_tweets_sentiment_json\citi_test'+yr+mth+'.json', 'w') as fp:
            json.dump(filter_tweet_list, fp)
#%%   
#SP
if not os.path.exists('sentimentdata\sp_tweets_sentiment_csv'):
    os.makedirs('sentimentdata\sp_tweets_sentiment_csv')
if not os.path.exists('sentimentdata\sp_tweets_sentiment_json'):
    os.makedirs('sentimentdata\sp_tweets_sentiment_json')
            
for yr in year:
    for mth in tqdm(month):
        filter_tweet_list = []
        text_list = []
        with open(tweets_path+'\spcleanjson\sp_tweets_removeduplicates_'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            for i in data:
                text_list.append(i[2])
            sentiment = getPrediction(text_list)
            for i in tqdm(range(len(data))):
                dic = {}
                dic['username'] = str(data[i][0])
                dic['date'] = str(data[i][1])
                dic['text'] = str(data[i][2])
                dic['sentiment'] = str(sentiment[i][2])
                dic['confidence_1'] = str(sentiment[i][1][0])
                dic['confidence_2'] = str(sentiment[i][1][1])
                filter_tweet_list.append(dic)
                
        keys = filter_tweet_list[0].keys()        
        with open('sentimentdata\sp_tweets_sentiment_csv\sp'+yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(filter_tweet_list)
        
        with open('sentimentdata\sp_tweets_sentiment_json\sp'+yr+mth+'.json', 'w') as fp:
            json.dump(filter_tweet_list, fp)
            
#%%   
#SPY
month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
year = ['14']
if not os.path.exists('sentimentdata\spy_tweets_sentiment_csv'):
    os.makedirs('sentimentdata\spy_tweets_sentiment_csv')
if not os.path.exists('sentimentdata\spy_tweets_sentiment_json'):
    os.makedirs('sentimentdata\spy_tweets_sentiment_json')
            
for yr in year:
    for mth in tqdm(month):
        filter_tweet_list = []
        text_list = []
        with open(tweets_path+'\spycleanjson\spy_tweets_removeduplicates_'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            for i in data:
                text_list.append(i[2])
            print('length: ' + str(len(text_list)))
            sentiment = getPrediction(text_list)
            print("HERE5")
            for i in tqdm(range(len(data))):
                dic = {}
                dic['username'] = str(data[i][0])
                dic['date'] = str(data[i][1])
                dic['text'] = str(data[i][2])
                dic['sentiment'] = str(sentiment[i][2])
                dic['confidence_1'] = str(sentiment[i][1][0])
                dic['confidence_2'] = str(sentiment[i][1][1])
                filter_tweet_list.append(dic)
                
        keys = filter_tweet_list[0].keys()        
        with open('sentimentdata\spy_tweets_sentiment_csv\sp'+yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(filter_tweet_list)
        
        with open('sentimentdata\spy_tweets_sentiment_json\sp'+yr+mth+'.json', 'w') as fp:
            json.dump(filter_tweet_list, fp)
#%%
import os

print(os.getcwd())
#os.chdir(r"C:\Users\Lawrann\Desktop\fyp3\Bert_NLP\sentiment_analysis")
#os.chdir(r"..\BERT_NLP\sentiment_analysis")
print(os.getcwd())

#%%
# Testing
for yr in year:
    for mth in month:
        filter_tweet_list = []
        text_list = []
        with open(tweets_path+'\spycleanjson\spy_tweets_removeduplicates_'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            for i in data:
                text_list.append(i[2])
        print(str(yr) + str(mth) + ':' + str(len(text_list)))
#%%
pred_sentences = [
"s&p",
"test",
"workin"
]

predictions = getPrediction(pred_sentences)
#%%
print(predictions)
