# -*- coding: utf-8 -*-

import json
import csv
import os
import re,string

def strip_links(text):

    pic_regex = re.compile('pic\.twitter\.com/(?:[^\ ]*)', re.DOTALL)
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ' ')  
    links = re.findall(pic_regex, text)
    for link in links:
        text = text.replace(link, '')
    text = text.replace(',#', ' #')
    return text

def strip_all_entities(text, tweet_terms, replace_term):
    for term in tweet_terms:
        text = text.replace(term, replace_term)
    entity_prefixes = ['@','#', '$']
#    for separator in  string.punctuation:
#        if separator not in entity_prefixes :
#            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    text = ' '.join(words)
    text = text.replace(' ,', '')
    text = text.replace(' , ', ' ')
    return text

month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
year = ['14','15','16','17','18']

#%%
#SP
if not os.path.exists('clean2\spcleancsv'):
    os.makedirs('clean2\spcleancsv')
if not os.path.exists('clean2\spcleanjson'):
    os.makedirs('clean2\spcleanjson')
    
sp_terms = ["S&P 500", "s&p 500", "s&p500", "S&P500", "indexsp", "INDEXSP"] # replace to S&P

for mth in month:
    for yr in year:
        filter_tweet_list = []
        with open('clean1\spcleanjson\sp_tweets_removeunwantedheaders_'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            for i in data:
                dic = {}
                dic['username'] = i['username']
                dic['date'] = i['date']
                dic['text'] = strip_all_entities(strip_links(i['text'].lower()), sp_terms, 's&p')
                filter_tweet_list.append(dic)

        keys = filter_tweet_list[0].keys()        
        with open('clean2\spcleancsv\sp_tweets_removelinks_'+yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(filter_tweet_list)
        with open('clean2\spcleanjson\sp_tweets_removelinks_'+yr+mth+'.json', 'w') as fp:
            json.dump(filter_tweet_list, fp)
            
#%%
#CITI
if not os.path.exists('clean2\citicleancsv'):
    os.makedirs('clean2\citicleancsv')
if not os.path.exists('clean2\citicleanjson'):
    os.makedirs('clean2\citicleanjson')

citi_terms = ["$C", "$c", "nyse:c", "NYSE:C", "#citi ", "#citigroup", "#Citi ", "#Citigroup"] # replace to citigroup

for mth in month:
    for yr in year:
        filter_tweet_list = []
        with open('clean1\citicleanjson\citi_tweets_removeunwantedheaders_'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            for i in data:
                dic = {}
                dic['username'] = i['username']
                dic['date'] = i['date']
                dic['text'] = strip_all_entities(strip_links(i['text']).lower(), citi_terms, 'citigroup')
                filter_tweet_list.append(dic)
        
        keys = filter_tweet_list[0].keys()        
        with open('clean2\citicleancsv\citi_tweets_removelinks_'+yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(filter_tweet_list)
        
        with open('clean2\citicleanjson\citi_tweets_removelinks_'+yr+mth+'.json', 'w') as fp:
            json.dump(filter_tweet_list, fp)
              
#%%
#SPY

month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
year = ['18']
            
if not os.path.exists('clean2\spycleancsv'):
    os.makedirs('clean2\spycleancsv')
if not os.path.exists('clean2\spycleanjson'):
    os.makedirs('clean2\spycleanjson')

spy_terms = ["S&P 500", "s&p 500", "s&p500", "S&P500", "SPDR S&P 500 Trust ETF", "$SPY"]

for mth in month:
    for yr in year:
        filter_tweet_list = []
        with open('clean1\spycleanjson\spy_tweets_removeunwantedheaders_'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            for i in data:
                dic = {}
                dic['username'] = i['username']
                dic['date'] = i['date']
                dic['text'] = strip_all_entities(strip_links(i['text'].lower()), spy_terms, 's&p')
                filter_tweet_list.append(dic)

        keys = filter_tweet_list[0].keys()        
        with open('clean2\spycleancsv\spy_tweets_removelinks_'+yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(filter_tweet_list)
        with open('clean2\spycleanjson\spy_tweets_removelinks_'+yr+mth+'.json', 'w') as fp:
            json.dump(filter_tweet_list, fp)
#%%
#SPY2

month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
year = ['14','15','16','17','18']
            
if not os.path.exists('clean2\spycleancsv'):
    os.makedirs('clean2\spycleancsv')
if not os.path.exists('clean2\spycleanjson'):
    os.makedirs('clean2\spycleanjson')

spy_terms = ["S&P 500", "s&p 500", "s&p500", "S&P500", "SPDR S&P 500 Trust ETF", "$SPY"]

for mth in month:
    for yr in year:
        filter_tweet_list = []
        with open('clean1\spycleanjson\spy_tweets_removeunwantedheaders_'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            for i in data:
                dic = {}
                dic['username'] = i['username']
                dic['date'] = i['date']
                dic['text'] = strip_all_entities(strip_links(i['text'].lower()), spy_terms, '')
                filter_tweet_list.append(dic)

        keys = filter_tweet_list[0].keys()        
        with open('clean2\spycleancsv\spy2_tweets_removelinks_'+yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(filter_tweet_list)
        with open('clean2\spycleanjson\spy2_tweets_removelinks_'+yr+mth+'.json', 'w') as fp:
            json.dump(filter_tweet_list, fp)
#%%
#ATVI
month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
year = ['14','15','16','17','18']
            
if not os.path.exists(r'clean2\atvicleancsv'):
    os.makedirs(r'clean2\atvicleancsv')
if not os.path.exists(r'clean2\atvicleanjson'):
    os.makedirs(r'clean2\atvicleanjson')

spy_terms = ["activision", "blizzard inc", "blizzard", "$ATVI", "#ATVI", "ATVI"]

for mth in month:
    for yr in year:
        filter_tweet_list = []
        with open(r'clean1\atvicleanjson\atvi_tweets_removeunwantedheaders_'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            for i in data:
                dic = {}
                dic['username'] = i['username']
                dic['date'] = i['date']
                dic['text'] = strip_all_entities(strip_links(i['text'].lower()), spy_terms, '')
                filter_tweet_list.append(dic)

        keys = filter_tweet_list[0].keys()        
        with open(r'clean2\atvicleancsv\atvi_tweets_removelinks_'+yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(filter_tweet_list)
        with open(r'clean2\atvicleanjson\atvi_tweets_removelinks_'+yr+mth+'.json', 'w') as fp:
            json.dump(filter_tweet_list, fp)
