# -*- coding: utf-8 -*-

import json
import csv
import os

stocks = ['atvi', 'citi', 'sp']
clean_path = 'articles_cleaned'
scrapped_path = 'articles_scrapped'

for stock in stocks:
    cpath = clean_path + '\\' + stock + '_articles\\' + stock + '_articles_cleaned.json'
    spath = scrapped_path + '\\' + stock + '_articles\\' + stock + '_articles_uncleaned.json'
    with open(cpath) as json_file:
        data = json.load(json_file) 
        print(stock + ' clean ' + str(len(data)))
    with open(spath) as json_file:
        data = json.load(json_file) 
        print(stock + ' scrapped ' + str(len(data)))

