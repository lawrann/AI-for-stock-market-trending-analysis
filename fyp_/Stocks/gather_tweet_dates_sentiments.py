# -*- coding: utf-8 -*-

# Gathering accumalated sentiment score for each date within the tweets json files

import json
import csv
from datetime import datetime 
from tqdm import tqdm


def unique(list1): 
    list_set = set(list1) 
    unique_list = (list(list_set)) 
    return unique_list

def printDates(dates):  
    for i in range(len(dates)):
        print(dates[i])  

def assign_sentiment_scores(source_folder, source_file_name, dest_folder, dest_file_name):
    ## get the sentiment scores
    month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
    year = ['14','15','16','17','18']
    date_list = []
    date_sentiment_list = []
    for yr in year:
        for mth in month:
            with open(source_folder + '\\' + source_file_name +yr+mth+'.json') as json_file:
                data = json.load(json_file)
                for i in data: # 'username', 'date', 'text', 'sentiment', 'confidence_1', 'confidence_2'
                    date_list.append(i['date'])
                    date_sentiment_list.append((i['date'],i['sentiment']))
    date_list = unique(date_list)
    date_list.sort(key = lambda date: datetime.strptime(date, '%Y-%m-%d')) 
    
    unique_date_sentiment_list = []
    unique_date_sentiment_list.append(('date','sentiment'))
    
    for date in tqdm(date_list, position=0, leave=True):
        runner_count = 0
        sentiment_score = 0
        num_tweets = 0
        while runner_count < len(date_sentiment_list):
            if date == date_sentiment_list[runner_count][0]:
                sentiment_score = sentiment_score + int(date_sentiment_list[runner_count][1])
                num_tweets = num_tweets + 1
            runner_count = runner_count + 1
        aggregate_sentiment_score = sentiment_score/num_tweets
        unique_date_sentiment_list.append((date, aggregate_sentiment_score))

    with open(dest_folder + '\\' + dest_file_name + '.csv', 'w', newline='', encoding='utf-8') as dest_file:
        csv_writer = csv.writer(dest_file, quoting=csv.QUOTE_ALL)
        for data in unique_date_sentiment_list:
            csv_writer.writerow(data)


#%%
# SPY
assign_sentiment_scores(r'..\Bert_NLP\sentiment_analysis\sentimentdata_neutral\spy_tweets_sentiment_json', # source_folder
                        'spy', # source_name
                        'spy', # dest folder
                        'spy_senti_scores_for_all_dates', # Store in the main stock price csv. split done after
                        )
#%%
# CITI
assign_sentiment_scores(r'..\Bert_NLP\sentiment_analysis\sentimentdata_neutral\citi_tweets_sentiment_json', # source_folder
                        'citi', # source_name
                        'citi', # dest folder
                        'citi_senti_scores_for_all_dates', # Store in the main stock price csv. split done after
                        )
#%%
# ATVI
assign_sentiment_scores(r'..\Bert_NLP\sentiment_analysis\sentimentdata_neutral\atvi_tweets_sentiment_json', # source_folder
                        'atvi', # source_name
                        'atvi', # dest folder
                        'atvi_senti_scores_for_all_dates', # Store in the main stock price csv. split done after
                        )
#%%
import os
os.chdir(r'C:\Users\Lawrann\Desktop\fyp_final\Stocks')
print(os.getcwd())