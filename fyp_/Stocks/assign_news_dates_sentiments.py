# -*- coding: utf-8 -*-

# Gathering accumalated sentiment score for each date within the articles json files

import json
import csv
from datetime import datetime 
from tqdm import tqdm

#%%
def unique(list1): 
    list_set = set(list1) 
    unique_list = (list(list_set)) 
    return unique_list

def printDates(dates):  
    for i in range(len(dates)):
        print(dates[i])  
        
#%%
def assign_sentiment_scores(source_folder, source_file_name, copy_source_file_name, dest_folder, dest_file_name):
    date_list = []
    date_sentiment_list = []
    
    unique_date_sentiment_list = [] # hold the tuple(date, sentiment_score)
    
    with open(source_folder + '\\' + source_file_name) as json_file:
        data = json.load(json_file)
        for i in data:
            date_list.append(i['date'])
            date_sentiment_list.append((i['date'],i['sentiment']))
        
    date_list = unique(date_list)
    date_list.sort(key = lambda date: datetime.strptime(date, '%Y-%m-%d')) 
    
    for date in tqdm(date_list, position=0, leave=True):
        runner_count = 0
        sentiment_score = 0
        while runner_count < len(date_sentiment_list):
            if date == date_sentiment_list[runner_count][0]:
                sentiment_score = sentiment_score + int(date_sentiment_list[runner_count][1])
            runner_count = runner_count + 1
        unique_date_sentiment_list.append((date, sentiment_score))
        
    holder_list = []
    stock_date_list = [] # stores the trading days
    
    with open(copy_source_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            holder_list.append(row[0])
        holder_list = holder_list[1:]
    
    for i in holder_list:
        ## Swap depending on how the date is stored.
        stock_date_list.append(i)
#        stock_date_list.append(datetime.strptime(i, '%m/%d/%Y').strftime('%Y-%m-%d'))
        
    final_date_sentiment_list = []
    get_date_list = []
    get_sentiment_list = []
    for i in unique_date_sentiment_list:
        get_date_list.append(i[0])
        get_sentiment_list.append(i[1])

    runner = 0
    for header in range(len(stock_date_list)):
        sentiment_score = 0
        if (stock_date_list[header] in get_date_list[runner:]):
            while (stock_date_list[header] in get_date_list[runner:]):
                if (get_date_list[runner] == stock_date_list[header]):
                    sentiment_score = sentiment_score + int(get_sentiment_list[runner])
                    final_date_sentiment_list.append((stock_date_list[header],sentiment_score))
                else:
                    sentiment_score = sentiment_score + int(get_sentiment_list[runner])
                runner = runner + 1
        else:
            final_date_sentiment_list.append((stock_date_list[header],sentiment_score))
            
    copy_list = []
    with open(copy_source_file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            copy_list.append(row)
        copy_list = copy_list[1:]
        
    for index in range(len(copy_list)):
        copy_list[index].append(str(final_date_sentiment_list[index][1]))
    
    with open(dest_folder + '\\' + dest_file_name, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        csv_writer.writerow(("Date","Open","High","Low","Close","Adj Close","Volume","Tweet_Sentiment", "Article_Sentiment"))
        for data in copy_list:
            if int(data[-1]) > 0:
                data[-1] = '1'
            elif int(data[-1]) < 0 :
                data[-1] = '-1'
            else: 
                data[-1] = '0'
                
            csv_writer.writerow(data)
        
    return final_date_sentiment_list
#%%
# using vader sentiment scoring

test_list = assign_sentiment_scores(r'..\Articles\articles_cleaned\atvi_articles', # source_folder
                        r'atvi_articles_cleaned.json', # source_file_name
                        r'atvi\atvi_Sentiment.csv',# copy_source_file_name
                        r'atvi', # dest_folder
                        r'atvi_Sentiment_Final.csv', # Store in the main stock price csv. split done after
                        )
#%%
# using vader sentiment scoring

test_list = assign_sentiment_scores(r'..\Articles\articles_cleaned\sp_articles', # source_folder
                        r'sp_articles_cleaned.json', # source_file_name
                        r'spy\spy_Sentiment.csv',# copy_source_file_name
                        r'spy', # dest_folder
                        r'spy_Sentiment_Final.csv', # Store in the main stock price csv. split done after
                        )
#%%
# using vader sentiment scoring

test_list = assign_sentiment_scores(r'..\Articles\articles_cleaned\citi_articles', # source_folder
                        r'citi_articles_cleaned.json', # source_file_name
                        r'citi\citi_Sentiment.csv',# copy_source_file_name
                        r'citi', # dest_folder
                        r'citi_Sentiment_Final.csv', # Store in the main stock price csv. split done after
                        )
#%%
import os

print(os.getcwd())
os.chdir(r"C:\Users\Lawrann\Desktop\fyp4\Stocks")
print(os.getcwd())