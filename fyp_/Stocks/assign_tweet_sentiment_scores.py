# -*- coding: utf-8 -*-

import csv
from datetime import datetime

#%% 
def assign_tweet_sentiment(stock_name):
    STOCK_NAME = stock_name
    holder_list = []
    stock_date_list = []
    with open(STOCK_NAME + '\\' + STOCK_NAME + '.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            holder_list.append(row[0])
        holder_list = holder_list[1:]
        
        for i in holder_list:
#            stock_date_list.append(i)
            stock_date_list.append(datetime.strptime(i, '%m/%d/%Y').strftime('%Y-%m-%d'))
            
    get_date_list = []
    get_sentiment_list = []
    with open(STOCK_NAME + '\\' + STOCK_NAME + '_senti_scores_for_all_dates.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            get_date_list.append(row[0])
            get_sentiment_list.append(row[1])
        get_date_list = get_date_list[1:]
        get_sentiment_list = get_sentiment_list[1:]
    
    final_date_sentiment_list = []
    runner = 0
    # stock_date_list, list of dates where stock exchange open
    # get_date_list, list of all dates with sentiment score in get_sentiment_list
    for header in range(len(stock_date_list)):
        sentiment_score = 0
        days_count = 0
        if (stock_date_list[header] in get_date_list[runner:]): # if exist
            while (stock_date_list[header] in get_date_list[runner:]):
                days_count =  days_count + 1
                if (get_date_list[runner] == stock_date_list[header]):
                    sentiment_score = sentiment_score + float(get_sentiment_list[runner])
                    if days_count == 0:
                        days_count = 1
                    final_sentiment_score = float(sentiment_score/days_count)
                    final_date_sentiment_list.append((stock_date_list[header],final_sentiment_score))
                else:
                    sentiment_score = sentiment_score + float(get_sentiment_list[runner])
                runner = runner + 1
        else: # if got stock_date but nnot in tweet
            if days_count == 0:
                days_count = 1
            final_sentiment_score = float(sentiment_score/days_count)
            final_date_sentiment_list.append((stock_date_list[header],final_sentiment_score))
                
    copy_list = []
    with open(STOCK_NAME + '\\' + STOCK_NAME +'.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            copy_list.append(row)
        copy_list = copy_list[1:]
    
    for index in range(len(copy_list)):
        copy_list[index].append(str(final_date_sentiment_list[index][1]))
     
    with open(STOCK_NAME + '\\' + STOCK_NAME + '_Sentiment.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        csv_writer.writerow(("Date","Open","High","Low","Close","Adj Close","Volume","Sentiment"))
        for data in copy_list:
            csv_writer.writerow(data)

#%%
#SPY
assign_tweet_sentiment('spy')
#%%
#CITI
assign_tweet_sentiment('citi')
#%%
#ATVI
assign_tweet_sentiment('atvi')
#%%
import os
os.chdir(r'C:\Users\Lawrann\Desktop\fyp_final\Stocks')
print(os.getcwd())