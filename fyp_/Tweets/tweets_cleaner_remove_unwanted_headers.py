# -*- coding: utf-8 -*-

import json
import csv
import os

month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
year = ['14','15','16','17','18']

cititweetscount = 0
sptweetscount = 0
spytweetscount = 0

#%%
#SP
if not os.path.exists('clean1\spcleancsv'):
    os.makedirs('clean1\spcleancsv')
if not os.path.exists('clean1\spcleanjson'):
    os.makedirs('clean1\spcleanjson')

for mth in month:
    for yr in year:
        filter_tweet_list = []
        with open('spdata\sp'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            for i in data:
                dic = {}
                dic['username'] = i['username']
                dic['date'] = i['timestamp'][0:10]
                dic['text'] = i['text']
                filter_tweet_list.append(dic)
        
        sptweetscount = sptweetscount + len(filter_tweet_list)
        keys = filter_tweet_list[0].keys()        
        with open('clean1\spcleancsv\sp_tweets_removeunwantedheaders_'+yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(filter_tweet_list)
        with open('clean1\spcleanjson\sp_tweets_removeunwantedheaders_'+yr+mth+'.json', 'w') as fp:
            json.dump(filter_tweet_list, fp)

print("Num of tweets for S&P500: " + str(sptweetscount))
    
#%%
#CITI
if not os.path.exists('clean1\citicleancsv'):
    os.makedirs('clean1\citicleancsv')
if not os.path.exists('clean1\citicleanjson'):
    os.makedirs('clean1\citicleanjson')
    
for mth in month:
    for yr in year:
        filter_tweet_list = []
        with open('citidata\citi'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            for i in data:
                dic = {}
                dic['username'] = i['username']
                dic['date'] = i['timestamp'][0:10]
                dic['text'] = i['text']
                filter_tweet_list.append(dic)
        
        cititweetscount = cititweetscount + len(filter_tweet_list)
        keys = filter_tweet_list[0].keys()        
        with open('clean1\citicleancsv\citi_tweets_removeunwantedheaders_'+yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(filter_tweet_list)
        
        with open('clean1\citicleanjson\citi_tweets_removeunwantedheaders_'+yr+mth+'.json', 'w') as fp:
            json.dump(filter_tweet_list, fp)
            
print("Num of tweets for Citi: " + str(cititweetscount))

#%%
#SPY
month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
#year = ['14','15','16','17','18']
year = ['18']

if not os.path.exists('clean1\spycleancsv'):
    os.makedirs('clean1\spycleancsv')
if not os.path.exists('clean1\spycleanjson'):
    os.makedirs('clean1\spycleanjson')
    
for mth in month:
    for yr in year:
        filter_tweet_list = []
        with open('spydata\spy'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            for i in data:
                dic = {}
                dic['username'] = i['username']
                dic['date'] = i['timestamp'][0:10]
                dic['text'] = i['text']
                filter_tweet_list.append(dic)
        
        spytweetscount = spytweetscount + len(filter_tweet_list)
        keys = filter_tweet_list[0].keys()        
        with open('clean1\spycleancsv\spy_tweets_removeunwantedheaders_'+yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(filter_tweet_list)
        
        with open('clean1\spycleanjson\spy_tweets_removeunwantedheaders_'+yr+mth+'.json', 'w') as fp:
            json.dump(filter_tweet_list, fp)
            
print("Num of tweets for Spy " + str(spytweetscount))
#%%
#ATVI
month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
year = ['14','15','16','17','18']

if not os.path.exists(r'clean1\atvicleancsv'):
    os.makedirs(r'clean1\atvicleancsv')
if not os.path.exists(r'clean1\atvicleanjson'):
    os.makedirs(r'clean1\atvicleanjson')
    
for mth in month:
    for yr in year:
        filter_tweet_list = []
        with open(r'atvidata\atvi'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            for i in data:
                dic = {}
                dic['username'] = i['username']
                dic['date'] = i['timestamp'][0:10]
                dic['text'] = i['text']
                filter_tweet_list.append(dic)
        
        spytweetscount = spytweetscount + len(filter_tweet_list)
        keys = filter_tweet_list[0].keys()        
        with open(r'clean1\atvicleancsv\atvi_tweets_removeunwantedheaders_'+yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(filter_tweet_list)
        
        with open(r'clean1\atvicleanjson\atvi_tweets_removeunwantedheaders_'+yr+mth+'.json', 'w') as fp:
            json.dump(filter_tweet_list, fp)
            
print("Num of tweets for ATVI " + str(spytweetscount))


