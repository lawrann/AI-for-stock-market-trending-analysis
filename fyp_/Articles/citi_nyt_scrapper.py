# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 02:05:28 2020

@author: Lawrann
"""
import os
import csv
import time
from nytimesarticle import articleAPI

api = articleAPI('pE4obr7qszOl3BziHDhS47RQv8ssf7pC')

if not os.path.exists('articles_scrapped\citi_articles'):
    os.makedirs('articles_scrapped\citi_articles')

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
    '''
    This function accepts a year in string format (e.g.'1980')
    and a query (e.g.'Amnesty International') and it will 
    return a list of parsed articles (in dictionaries)
    for that year.
    '''
    all_articles = []
    for i in range(0,100): #NYT limits pager to first 100 pages. But rarely will you find over 100 pages of results anyway. 
        print("==== Page " + str(i) + " Year " + date + " ====")
        
        articles1 = api.search(q = query,
               fq = {'source':['Reuters','AP', 'The New York Times']},
               begin_date = date + '0101',
               end_date = date + '0228',
               sort='oldest',
               page = str(i))
        articles1 = parse_articles(articles1)
        time.sleep(6)
        
        articles2 = api.search(q = query,
               fq = {'source':['Reuters','AP', 'The New York Times']},
               begin_date = date + '0301',
           end_date = date + '0430',
               sort='oldest',
               page = str(i))
        articles2 = parse_articles(articles2)
        time.sleep(6)
        
        articles3 = api.search(q = query,
               fq = {'source':['Reuters','AP', 'The New York Times']},
               begin_date = date + '0501',
           end_date = date + '0630',
               sort='oldest',
               page = str(i))
        articles3 = parse_articles(articles3)
        time.sleep(6)

        articles4 = api.search(q = query,
               fq = {'source':['Reuters','AP', 'The New York Times']},
               begin_date = date + '0701',
           end_date = date + '0831',
               sort='oldest',
               page = str(i))
        articles4 = parse_articles(articles4)
        time.sleep(6)
        
        articles5 = api.search(q = query,
               fq = {'source':['Reuters','AP', 'The New York Times']},
               begin_date = date + '0901',
           end_date = date + '1031',
               sort='oldest',
               page = str(i))
        articles5 = parse_articles(articles5)
        time.sleep(6)
        
        articles6 = api.search(q = query,
               fq = {'source':['Reuters','AP', 'The New York Times']},
               begin_date = date + '1101',
           end_date = date + '1231',
               sort='oldest',
               page = str(i))
        articles6 = parse_articles(articles6)
        time.sleep(6)
                
        all_articles = all_articles + articles1 + articles2 + articles3 + articles4 + articles5 + articles6
        
    return(all_articles)

Citi_all = []
for i in range(2014,2019):
    print('Processing ' + str(i) + '...')
    Citi_year =  get_articles(str(i),'Citi')
    Citi_all = Citi_all + Citi_year

keys = Citi_all[0].keys()
with open('articles_scrapped\citi_articles\citi_articles_uncleaned3.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(Citi_all)


import json
with open('articles_scrapped\citi_articles\citi_articles_uncleaned3.json', 'w') as fp:
    json.dump(Citi_all, fp)

                
