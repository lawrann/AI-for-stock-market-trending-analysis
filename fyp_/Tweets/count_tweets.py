# -*- coding: utf-8 -*-


import json
import csv
import os
#%%
# count number of tweets
stocks = ['citi','spy', 'atvi']
month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
year = ['14','15','16','17','18']

total = 0

for stock in stocks:
    stock_count = 0
    for yr in year:
        for mth in month:
            path = stock + 'data' + '\\' + stock + yr + mth + '.json'
            with open(path) as json_file:
                data = json.load(json_file)
                total = total + len(data)
                stock_count = stock_count + len(data)
    print('stock count ' + stock + ': ' + str(stock_count))

print('total count: ' + str(total))
#%%
# count after preprocessing
stocks = ['citi','spy', 'atvi']
month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
year = ['14','15','16','17','18']
total = 0
for stock in stocks:
    stock_count = 0
    for yr in year:
        for mth in month:
            path = 'clean3\\' + stock + 'cleanjson' + '\\' + stock + '_tweets_removeduplicates_' + yr + mth + '.json'
            with open(path) as json_file:
                data = json.load(json_file)
                total = total + len(data)
                stock_count = stock_count + len(data)
    print('stock count ' + stock + ': ' + str(stock_count))

print('total count: ' + str(total))

#%%
# count postive, neutral negative
#stocks = ['citi','spy', 'atvi']
#month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
#year = ['14','15','16','17','18']
stocks = ['citi']
month = ['01']
year = ['14']
total = 0
for stock in stocks:
    stock_count = 0
    for yr in year:
        for mth in month:
            path = 'clean3\\' + stock + 'cleanjson' + '\\' + stock + '_tweets_removeduplicates_' + yr + mth + '.json'
            with open(path) as json_file:
                data = json.load(json_file)
                for i in data:
                    print(i[0])
                total = total + len(data)
                stock_count = stock_count + len(data)
    print('stock count ' + stock + ': ' + str(stock_count))

print('total count: ' + str(total))
#%%

import os

os.chdir(r'C:\Users\Lawrann\Desktop\fyp_final\Tweets')
print(os.getcwd())