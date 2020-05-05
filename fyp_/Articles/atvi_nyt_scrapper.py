# -*- coding: utf-8 -*-

import os
import csv
import time
from nytimesarticle import articleAPI

api = articleAPI('pE4obr7qszOl3BziHDhS47RQv8ssf7pC')

if not os.path.exists('articles_scrapped\sp_articles'):
    os.makedirs('articles_scrapped\sp_articles')

def parse_articles(articles):
    news = []
    if (articles.get("response") is not None) and ((articles.get("response")).get("docs") is not None):
        for i in articles['response']['docs']:
            dic = {}
            dic['id'] = i['_id']
            if i['abstract'] is not None:
                dic['abstract'] = i['abstract']
            dic['headline'] = i['headline']['main']
            dic['desk'] = i['news_desk']
            dic['date'] = i['pub_date'][0:10] # cutting time of day.
            dic['section'] = i['section_name']
            if i['snippet'] is not None:
                dic['snippet'] = i['snippet']
            if i['lead_paragraph'] is not None:
                dic['lead_paragraph'] = i['lead_paragraph']
            dic['source'] = i['source']
            dic['type'] = i['type_of_material']
            dic['url'] = i['web_url']
            dic['word_count'] = i['word_count']
            # locations
            locations = []
            for x in range(0,len(i['keywords'])):
                if 'glocations' in i['keywords'][x]['name']:
                    locations.append(i['keywords'][x]['value'])
            dic['locations'] = locations
            # subject
            subjects = []
            for x in range(0,len(i['keywords'])):
                if 'subject' in i['keywords'][x]['name']:
                    subjects.append(i['keywords'][x]['value'])
            dic['subjects'] = subjects   
            news.append(dic)
    return(news) 

def get_articles(date,query):
    all_articles = []
    for i in range(0,100): #NYT limits pager to first 100 pages. But rarely will you find over 100 pages of results anyway. 
        print("==== Page " + str(i) + " for year " + str(date) + " ====")
        
        articles1 = api.search(q = query,
               fq = {'source':['Reuters','AP', 'The New York Times']},
               begin_date = date + '0101',
               end_date = date + '0630',
               sort='oldest',
               page = str(i))
        articles1 = parse_articles(articles1)
        time.sleep(6)
        
        articles2 = api.search(q = query,
           fq = {'source':['Reuters','AP', 'The New York Times']},
           begin_date = date + '0701',
           end_date = date + '1231',
           sort='oldest',
           page = str(i))
        articles2 = parse_articles(articles2)
        time.sleep(6)
        
        all_articles = all_articles + articles1 + articles2
        
        
    return(all_articles)

SP_all = []
for i in range(2014,2019):
    print('Processing ' + str(i) + '...')
    SP_year =  get_articles(str(i),'activision')
    SP_all = SP_all + SP_year

keys = SP_all[0].keys()

if not os.path.exists(r'articles_scrapped\atvi_articles'):
    os.makedirs(r'articles_scrapped\atvi_articles')

print(keys)
with open(r'articles_scrapped\atvi_articles\atvi_articles_uncleaned.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(SP_all)

import json
with open(r'articles_scrapped\atvi_articles\atvi_articles_uncleaned.json', 'w') as fp:
    json.dump(SP_all, fp)

#%%
import os
os.chdir(r'C:\Users\Lawrann\Desktop\fyp_final\Articles')
print(os.getcwd())