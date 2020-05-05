# -*- coding: utf-8 -*-

import json
import csv
import os
import re,string
from tqdm import tqdm
import pandas as pd 

def unique(list1): 
    # insert the list to the set 
    list_set = set(list1) 
    # convert the set to the list 
    unique_list = (list(list_set)) 
    
    return unique_list

month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
year = ['14','15','16','17','18']

#%%
#SP
if not os.path.exists('clean3\spcleancsv'):
    os.makedirs('clean3\spcleancsv')
if not os.path.exists('clean3\spcleanjson'):
    os.makedirs('clean3\spcleanjson')
    
sp_count = 0

for yr in year:
    for mth in month:
        with open('clean2\spcleanjson\sp_tweets_removelinks_'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            new_data = []
            tuple_list = []
            del_list = []
            for i in data: # keys: username, date, text
                tuple_list.append((i['username'],i['date'], i['text']))
                
            list_len = len(tuple_list)
            for header in tqdm(range(len(tuple_list)), position=0, leave=True):
                runner = header + 1
                while (runner<list_len and tuple_list[header][1] == tuple_list[runner][1]):
                    string_len = int(len(tuple_list[runner][2])*0.6)
                    if ((tuple_list[runner][2])[:string_len] in tuple_list[header][2]):
                        del_list.append(runner)
                    runner = runner + 1
                    
            tqdm.write("sp" + str(yr) + str(mth))
            tqdm.write("# Tweets Before: " + str(len(tuple_list)))
            del_list = unique(del_list)
            tqdm.write("# Duplicate: " + str(len(del_list)))
            del_list.sort()
            del_list.reverse()
            for i in del_list:
                del tuple_list[i]
            tqdm.write("# Tweets After: " + str(len(tuple_list)))
            sp_count = sp_count + int(len(tuple_list))
        
        with open('clean3\spcleancsv\sp_tweets_removeduplicates_'+yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
            df = pd.DataFrame(tuple_list)
            df.to_csv(output_file, header=False, index=False, encoding='utf-8')
        
        with open('clean3\spcleanjson\sp_tweets_removeduplicates_'+yr+mth+'.json', 'w') as fp:
            json.dump(tuple_list, fp)

print("Total tweets for SP " + str(sp_count))
#%%
#CITI
if not os.path.exists('clean3\citicleancsv'):
    os.makedirs('clean3\citicleancsv')
if not os.path.exists('clean3\citicleanjson'):
    os.makedirs('clean3\citicleanjson')
    
citi_count = 0    

for yr in year:
    for mth in month:
        with open('clean2\citicleanjson\citi_tweets_removelinks_'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            new_data = []
            tuple_list = []
            del_list = []
            for i in data: # keys: username, date, text
                tuple_list.append((i['username'],i['date'], i['text']))
                
            list_len = len(tuple_list)
            for header in tqdm(range(len(tuple_list)), position=0, leave=True):
                runner = header + 1
                while (runner<list_len and tuple_list[header][1] == tuple_list[runner][1]):
                    string_len = int(len(tuple_list[runner][2])*0.6)
                    if ((tuple_list[runner][2])[:string_len] in tuple_list[header][2]):
                        del_list.append(runner)
                    runner = runner + 1
                    
            tqdm.write("Citi" + str(yr) + str(mth))
            tqdm.write("# Tweets Before: " + str(len(tuple_list)))
            del_list = unique(del_list)
            tqdm.write("# Duplicate: " + str(len(del_list)))
            del_list.sort()
            del_list.reverse()
            for i in del_list:
                del tuple_list[i]
            tqdm.write("# Tweets After: " + str(len(tuple_list)))
            citi_count = citi_count + int(len(tuple_list))
        
        with open('clean3\citicleancsv\citi_tweets_removeduplicates_'+yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
            df = pd.DataFrame(tuple_list)
            df.to_csv(output_file, header=False, index=False, encoding='utf-8')
        
        with open('clean3\citicleanjson\citi_tweets_removeduplicates_'+yr+mth+'.json', 'w') as fp:
            json.dump(tuple_list, fp)

print("Total tweets for Citi " + str(citi_count))
#%%
#SPY
if not os.path.exists('clean3\spycleancsv'):
    os.makedirs('clean3\spycleancsv')
if not os.path.exists('clean3\spycleanjson'):
    os.makedirs('clean3\spycleanjson')
    
spy_count = 0


month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
year = ['18']

for yr in year:
    for mth in month:
        with open('clean2\spycleanjson\spy_tweets_removelinks_'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            new_data = []
            tuple_list = []
            del_list = []
            for i in data: # keys: username, date, text
                tuple_list.append((i['username'],i['date'], i['text']))
                
            list_len = len(tuple_list)
            for header in tqdm(range(len(tuple_list)), position=0, leave=True):
                runner = header + 1
                while (runner<list_len and tuple_list[header][1] == tuple_list[runner][1]):
                    string_len = int(len(tuple_list[runner][2])*0.6)
                    if ((tuple_list[runner][2])[:string_len] in tuple_list[header][2]):
                        del_list.append(runner)
                    runner = runner + 1
                    
            tqdm.write("spy" + str(yr) + str(mth))
            tqdm.write("# Tweets Before: " + str(len(tuple_list)))
            del_list = unique(del_list)
            tqdm.write("# Duplicate: " + str(len(del_list)))
            del_list.sort()
            del_list.reverse()
            for i in del_list:
                del tuple_list[i]
            tqdm.write("# Tweets After: " + str(len(tuple_list)))
            spy_count = spy_count + int(len(tuple_list))
        
        with open('clean3\spycleancsv\spy_tweets_removeduplicates_'+yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
            df = pd.DataFrame(tuple_list)
            df.to_csv(output_file, header=False, index=False, encoding='utf-8')
        
        with open('clean3\spycleanjson\spy_tweets_removeduplicates_'+yr+mth+'.json', 'w') as fp:
            json.dump(tuple_list, fp)

print("Total tweets for SPY " + str(spy_count))
#%%
#SPY2
if not os.path.exists('clean3\spycleancsv'):
    os.makedirs('clean3\spycleancsv')
if not os.path.exists('clean3\spycleanjson'):
    os.makedirs('clean3\spycleanjson')
    
spy_count = 0


month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
year = ['14','15','16','17','18']

for yr in year:
    for mth in month:
        with open('clean2\spycleanjson\spy2_tweets_removelinks_'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            new_data = []
            tuple_list = []
            del_list = []
            for i in data: # keys: username, date, text
                tuple_list.append((i['username'],i['date'], i['text']))
                
            list_len = len(tuple_list)
            for header in tqdm(range(len(tuple_list)), position=0, leave=True):
                runner = header + 1
                while (runner<list_len and tuple_list[header][1] == tuple_list[runner][1]):
                    string_len = int(len(tuple_list[runner][2])*0.6)
                    if ((tuple_list[runner][2])[:string_len] in tuple_list[header][2]):
                        del_list.append(runner)
                    runner = runner + 1
                    
            tqdm.write("spy" + str(yr) + str(mth))
            tqdm.write("# Tweets Before: " + str(len(tuple_list)))
            del_list = unique(del_list)
            tqdm.write("# Duplicate: " + str(len(del_list)))
            del_list.sort()
            del_list.reverse()
            for i in del_list:
                del tuple_list[i]
            tqdm.write("# Tweets After: " + str(len(tuple_list)))
            spy_count = spy_count + int(len(tuple_list))
        
        with open('clean3\spycleancsv\spy2_tweets_removeduplicates_'+yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
            df = pd.DataFrame(tuple_list)
            df.to_csv(output_file, header=False, index=False, encoding='utf-8')
        
        with open('clean3\spycleanjson\spy2_tweets_removeduplicates_'+yr+mth+'.json', 'w') as fp:
            json.dump(tuple_list, fp)

print("Total tweets for SPY " + str(spy_count))

#%%
#ATVI
if not os.path.exists(r'clean3\atvicleancsv'):
    os.makedirs(r'clean3\atvicleancsv')
if not os.path.exists(r'clean3\atvicleanjson'):
    os.makedirs(r'clean3\atvicleanjson')
    
spy_count = 0


month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
year = ['14','15','16','17','18']

for yr in year:
    for mth in month:
        with open(r'clean2\atvicleanjson\atvi_tweets_removelinks_'+yr+mth+'.json') as json_file:
            data = json.load(json_file)
            new_data = []
            tuple_list = []
            del_list = []
            for i in data: # keys: username, date, text
                tuple_list.append((i['username'],i['date'], i['text']))
                
            list_len = len(tuple_list)
            for header in tqdm(range(len(tuple_list)), position=0, leave=True):
                runner = header + 1
                while (runner<list_len and tuple_list[header][1] == tuple_list[runner][1]):
                    string_len = int(len(tuple_list[runner][2])*0.6)
                    if ((tuple_list[runner][2])[:string_len] in tuple_list[header][2]):
                        del_list.append(runner)
                    runner = runner + 1
                    
            tqdm.write("atvi" + str(yr) + str(mth))
            tqdm.write("# Tweets Before: " + str(len(tuple_list)))
            del_list = unique(del_list)
            tqdm.write("# Duplicate: " + str(len(del_list)))
            del_list.sort()
            del_list.reverse()
            for i in del_list:
                del tuple_list[i]
            tqdm.write("# Tweets After: " + str(len(tuple_list)))
            spy_count = spy_count + int(len(tuple_list))
        
        with open(r'clean3\atvicleancsv\atvi_tweets_removeduplicates_'+yr+mth+'.csv', 'w', newline='', encoding='utf-8') as output_file:
            df = pd.DataFrame(tuple_list)
            df.to_csv(output_file, header=False, index=False, encoding='utf-8')
        
        with open(r'clean3\atvicleanjson\atvi_tweets_removeduplicates_'+yr+mth+'.json', 'w') as fp:
            json.dump(tuple_list, fp)

print("Total tweets for ATVI " + str(spy_count))
#%%
# count tweets
        
import json
import csv
import os
import re,string
from tqdm import tqdm
import pandas as pd 

month = ['01','02','03','04','05','06','07','08','09','10','11','12',]
year = ['14','15','16','17','18']
total = 0
for yr in year:
    for mth in month:
        with open(r'C:\Users\Lawrann\Desktop\fyp2\Tweets\clean3\citicleanjson\citi_tweets_removeduplicates_'+yr+mth+'.json', 'r') as json_file:
            data = json.load(json_file)
            total = total + len(data)
            print("citi"+str(yr)+str(mth)+" "+str(len(data)))
print("total: " + str(total))

for yr in year:
    for mth in month:
        with open(r'C:\Users\Lawrann\Desktop\fyp2\Tweets\clean3\spcleanjson\sp_tweets_removeduplicates_'+yr+mth+'.json', 'r') as json_file:
            data = json.load(json_file)
            total = total + len(data)
            print("sp"+str(yr)+str(mth)+" "+str(len(data)))
print("total: " + str(total))

