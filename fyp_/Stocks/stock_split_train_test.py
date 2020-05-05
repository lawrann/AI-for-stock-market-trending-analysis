# -*- coding: utf-8 -*-

import csv
from datetime import datetime 
from tqdm import tqdm
#%%

def split_train_test_csv(source_filepath, dest_folder, num_training_records, train_name, test_name):
    
    train_list = []
    test_list = []
    
    with open(source_filepath, 'r') as source:
        reader = csv.reader(source)
        headers = next(reader)  
        columns = headers
        train_list.append(columns)
        test_list.append(columns)
        headers = next(reader) # skip the headers
        for i in range(num_training_records):
            train_list.append(headers)
            headers = next(reader)
        
        while 1:
            test_list.append(headers)
            try:
                headers = next(reader)
            except:
                break
    with open(dest_folder + '\\' + train_name + '.csv', 'w', newline='', encoding='utf-8') as train_file:
        csv_writer = csv.writer(train_file, quoting=csv.QUOTE_ALL)
        for data in train_list:
            csv_writer.writerow(data)
        
    with open(dest_folder + '\\' + test_name + '.csv', 'w', newline='', encoding='utf-8') as test_file:
        csv_writer = csv.writer(test_file, quoting=csv.QUOTE_ALL)
        for data in test_list:
            csv_writer.writerow(data)

#%%
# Change num_training_records according to ur number of training records.
# The rest will be testing set
# source_filepath, dest_folder, num_training_records, train_name, test_name
#%%
#SPY
split_train_test_csv('spy\spy_Sentiment_Final.csv', 'spy', 1007, 'spy_train', 'spy_test')
#%%
#Citi
split_train_test_csv('citi\citi_Sentiment_Final.csv', 'citi', 1007, 'citi_train', 'citi_test')
#%%
#Atvi
split_train_test_csv(r'atvi\atvi_Sentiment_Final.csv', 'atvi', 1007, 'atvi_train', 'atvi_test')
#%%

