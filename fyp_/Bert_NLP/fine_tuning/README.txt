BERT Fine Tuning using sentiment140 dataset obtained from kaggle

- bert_training_test_shuffle.ipynb is for generating the shuffled twitter test and train dataset in .json format
- bert_finetune_tf_hub.ipynb is for fine tuning bert model using google collab.
- bert_finetune_tf_hub.py is for fine tuning our bert model using local gpu (Slower).

How to run:
1) Upload training1600000.csv to google drive. path @ r"drive/My Drive"

2) Upload and run notebook bert_training_test_shuffle.ipynb to google collab.
- This will create "bert_train_test_csv" and "bert_train_test_json" folder within 
- your google drive which contain the test and train data.
Otherwise, you can upload the populated "bert_train_test_csv" and "bert_train_test_json" folder 
to google drive path @ r"drive/My Drive" to skip the generation of test and train dataset.

3) Upload and run notebook bert_finetune_tf_hub.ipynb on google collab to beging finetuning the Bert model
- To further finetune my finetuned model, upload folder bert_model to google drive r"drive/My Drive" and run bert_finetune_tf_hub.ipynb 

Google collab had to be used because my local GPU has insufficient memory for fine tuning the BERT model.