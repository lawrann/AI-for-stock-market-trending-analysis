# -*- coding: utf-8 -*-

import json
import csv
import os
from datetime import datetime 
from tqdm import tqdm

month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
year = ['14','15','16','17','18']

#%%
#SPY
stock_name = 'spy'
source_folder = 'sentimentdata\\' + stock_name + '_tweets_sentiment_json'
source_file_name = stock_name
dest_folder_json = 'sentimentdata_neutral\\' + stock_name + '_tweets_sentiment_json'
dest_folder_csv = 'sentimentdata_neutral\\' + stock_name + '_tweets_sentiment_csv'
dest_file_name = stock_name

if not os.path.exists('sentimentdata_neutral'):
    os.makedirs('sentimentdata_neutral')
if not os.path.exists(dest_folder_json):
    os.makedirs(dest_folder_json)
if not os.path.exists(dest_folder_csv):
    os.makedirs(dest_folder_csv)


for yr in year:
        for mth in month:
            filter_tweet_list = []
            with open(source_folder + '\\' + source_file_name +yr+mth+'.json') as json_file:
                data = json.load(json_file) #dict_keys(['username', 'date', 'text', 'sentiment', 'confidence_1', 'confidence_2'])
                for i in data:
                    dic = {}
                    dic['username'] = i['username']
                    dic['date'] = i['date']
                    dic['text'] = i['text']
                    dic['confidence_1'] = i['confidence_1']
                    dic['confidence_2'] = i['confidence_2']
                    c1 = float(i['confidence_1']) # negative confidence
                    c2 = float(i['confidence_2']) # positive confidence
                    confidence = c2-c1
                    if (confidence > -0.3 and confidence < 0.3):
                        dic['sentiment'] = 0
                    else:
                        dic['sentiment'] = i['sentiment']
                    filter_tweet_list.append(dic)
            keys = filter_tweet_list[0].keys() 
            with open(dest_folder_csv + '\\' + dest_file_name +yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(filter_tweet_list)
        
            with open(dest_folder_json + '\\' + dest_file_name +yr+mth+'.json', 'w') as fp:
                json.dump(filter_tweet_list, fp)
                
#%%
#ATVI
stock_name = 'atvi'
source_folder = 'sentimentdata\\' + stock_name + '_tweets_sentiment_json'
source_file_name = stock_name
dest_folder_json = 'sentimentdata_neutral\\' + stock_name + '_tweets_sentiment_json'
dest_folder_csv = 'sentimentdata_neutral\\' + stock_name + '_tweets_sentiment_csv'
dest_file_name = stock_name

if not os.path.exists('sentimentdata_neutral'):
    os.makedirs('sentimentdata_neutral')
if not os.path.exists(dest_folder_json):
    os.makedirs(dest_folder_json)
if not os.path.exists(dest_folder_csv):
    os.makedirs(dest_folder_csv)


for yr in year:
        for mth in month:
            filter_tweet_list = []
            with open(source_folder + '\\' + source_file_name +yr+mth+'.json') as json_file:
                data = json.load(json_file) #dict_keys(['username', 'date', 'text', 'sentiment', 'confidence_1', 'confidence_2'])
                for i in data:
                    dic = {}
                    dic['username'] = i['username']
                    dic['date'] = i['date']
                    dic['text'] = i['text']
                    dic['confidence_1'] = i['confidence_1']
                    dic['confidence_2'] = i['confidence_2']
                    c1 = float(i['confidence_1']) # negative confidence
                    c2 = float(i['confidence_2']) # positive confidence
                    confidence = c2-c1
                    if (confidence > -0.3 and confidence < 0.3):
                        dic['sentiment'] = 0
                    else:
                        dic['sentiment'] = i['sentiment']
                    filter_tweet_list.append(dic)
            keys = filter_tweet_list[0].keys() 
            with open(dest_folder_csv + '\\' + dest_file_name +yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(filter_tweet_list)
        
            with open(dest_folder_json + '\\' + dest_file_name +yr+mth+'.json', 'w') as fp:
                json.dump(filter_tweet_list, fp)
#%%
#CITI
stock_name = 'citi'
source_folder = 'sentimentdata\\' + stock_name + '_tweets_sentiment_json'
source_file_name = stock_name
dest_folder_json = 'sentimentdata_neutral\\' + stock_name + '_tweets_sentiment_json'
dest_folder_csv = 'sentimentdata_neutral\\' + stock_name + '_tweets_sentiment_csv'
dest_file_name = stock_name

if not os.path.exists('sentimentdata_neutral'):
    os.makedirs('sentimentdata_neutral')
if not os.path.exists(dest_folder_json):
    os.makedirs(dest_folder_json)
if not os.path.exists(dest_folder_csv):
    os.makedirs(dest_folder_csv)


for yr in year:
        for mth in month:
            filter_tweet_list = []
            with open(source_folder + '\\' + source_file_name +yr+mth+'.json') as json_file:
                data = json.load(json_file) #dict_keys(['username', 'date', 'text', 'sentiment', 'confidence_1', 'confidence_2'])
                for i in data:
                    dic = {}
                    dic['username'] = i['username']
                    dic['date'] = i['date']
                    dic['text'] = i['text']
                    dic['confidence_1'] = i['confidence_1']
                    dic['confidence_2'] = i['confidence_2']
                    c1 = float(i['confidence_1']) # negative confidence
                    c2 = float(i['confidence_2']) # positive confidence
                    confidence = c2-c1
                    if (confidence > -0.3 and confidence < 0.3):
                        dic['sentiment'] = 0
                    else:
                        dic['sentiment'] = i['sentiment']
                    filter_tweet_list.append(dic)
            keys = filter_tweet_list[0].keys() 
            with open(dest_folder_csv + '\\' + dest_file_name +yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(filter_tweet_list)
        
            with open(dest_folder_json + '\\' + dest_file_name +yr+mth+'.json', 'w') as fp:
                json.dump(filter_tweet_list, fp)
#%%
                
import os
print(os.getcwd())
os.chdir(r'C:\Users\Lawrann\Desktop\fyp_final\Bert_NLP\sentiment_analysis')
print(os.getcwd())