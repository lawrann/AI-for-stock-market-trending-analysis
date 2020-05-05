# -*- coding: utf-8 -*-

import json
import csv

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()

stock_name = 'citi'
path = 'articles_cleaned\\' + stock_name + '_articles\\' + stock_name + '_articles_cleaned.json' 

def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    # print(score.keys()) keys: 'neg', 'neu', 'pos', 'compound'
    print(score)
    neg = score['neg']
    pos = score['pos']
    if (pos>neg):
        return 1
    elif (neg>pos):
        return -1
    else:
        return 0

filter_article_list = []
with open(path) as json_file:
    data = json.load(json_file) 
    for i in data: # keys: 'date', 'abstract', 'headline', 'lead_paragraph', 'snippet'
        #print(i['headline'])
        dic = {}
        dic['date'] = i['date']
        dic['abstract'] = i['abstract']
        dic['headline'] = i['headline']
        dic['snippet'] = i['snippet']
        dic['lead_paragraph'] = i['lead_paragraph']
        
        abstract_sentiment = sentiment_analyzer_scores(i['abstract'])
        headline_sentiment = sentiment_analyzer_scores(i['headline'])
        snippet_sentiment = sentiment_analyzer_scores(i['snippet'])
        lead_paragraph_sentiment = sentiment_analyzer_scores(i['lead_paragraph'])
        
        dic['abstract_sentiment'] = abstract_sentiment
        dic['headline_sentiment'] = headline_sentiment
        dic['snippet_sentiment'] = snippet_sentiment
        dic['lead_paragraph_sentiment'] = lead_paragraph_sentiment
        
        final_sentiment = abstract_sentiment + headline_sentiment + snippet_sentiment + lead_paragraph_sentiment
        if (final_sentiment > 0):
            dic['sentiment'] = 1
        elif (final_sentiment < 0):
            dic['sentiment'] = -1
        else:
            dic['sentiment'] = 0
        filter_article_list.append(dic)
            
keys = filter_article_list[0].keys()
path2 = 'articles_cleaned\\'  + stock_name +'_articles\\' + stock_name +'_articles_cleaned.csv'
with open(path2, 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(filter_article_list)

with open(path, 'w') as fp:
    json.dump(filter_article_list, fp)
    

