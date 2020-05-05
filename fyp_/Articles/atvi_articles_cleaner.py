# -*- coding: utf-8 -*-
# For activision stocks, just filter by section for the articles

import json
import csv
import os

if not os.path.exists(r'articles_cleaned\atvi_articles'):
    os.makedirs(r'articles_cleaned\atvi_articles')

#filter_texts = ["activision", "blizzard", "atvi"]
# Remove irrelevant sections
filter_sections = ["fashion & style", "arts", "books", "food", "sports", "travel", "the upshot", "blogs", "opinion", "u.s.", "your money"]

def splitter(text):
    term_list = ['activision', 'atvi', 'blizzard']
    new_string = ''
    if '|' in text:
        split_list = text.split('|')
        new_string = ''
        for term in term_list:
            for split in split_list:
                if term in split.lower():
                    if split not in new_string:
                        if new_string == '':
                            new_string = split
                        else:
                            new_string = new_string + '|' + split
    elif ';' in text:
        split_list = text.split(';')
        new_string = ''
        for term in term_list:
            for split in split_list:
                if term in split.lower():
                    if split not in new_string:
                        if new_string == '':
                            new_string = split
                        else:
                            new_string = new_string + '|' + split
    else:
        return text
    if new_string == '':
        return text
    else:
        return new_string

with open(r'articles_scrapped\atvi_articles\atvi_articles_uncleaned.json') as json_file:
    data = json.load(json_file) 
    count = 1
    filter_article_list = []
    for i in data:
        enter_flag = True
        # dict_keys(['id', 'abstract', 'headline', 'desk', 'date', 'section', 'snippet', 'source', 'type', 'url', 'word_count', 'locations', 'subjects', lead_paragraph])
        for section in filter_sections:
            if section in i["section"].lower():
                enter_flag = False
        if enter_flag:
            dic = {}
            dic['id'] = i['id']
            if i['abstract'] is not None:   
                dic['abstract'] = splitter(i['abstract'])
            dic['headline'] = splitter(i['headline'])
            dic['desk'] = i['desk']
            dic['date'] = i['date'][0:10] # cutting time of day.
            dic['section'] = i['section']
            if i['snippet'] is not None:
                dic['snippet'] = splitter(i['snippet'])
            if i['lead_paragraph'] is not None:
                dic['lead_paragraph'] = splitter(i['lead_paragraph'])
            dic['source'] = i['source']
            dic['type'] = i['type']
            dic['url'] = i['url']
            dic['word_count'] = i['word_count']
            dic['locations'] = i['locations']
            dic['subjects'] = i['subjects']   
            filter_article_list.append(dic)
            enter_flag = False
            
keys = filter_article_list[0].keys()
with open(r'articles_cleaned\atvi_articles\atvi_articles_cleaned.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(filter_article_list)

with open(r'articles_cleaned\atvi_articles\atvi_articles_cleaned.json', 'w') as fp:
    json.dump(filter_article_list, fp)


with open(r'articles_cleaned\atvi_articles\atvi_articles_cleaned.json') as json_file:
    data = json.load(json_file) 
    count = 1
    filter_article_list = []
    for i in data:
        # dict_keys(['id', 'abstract', 'headline', 'desk', 'date', 'section', 'snippet', 'source', 'type', 'url', 'word_count', 'locations', 'subjects', lead_paragraph])

            dic = {}
            dic['date'] = i['date'][0:10] # cutting time of day.
            if i['abstract'] is not None:   
                dic['abstract'] = i['abstract']
            dic['headline'] = i['headline']
            if i['lead_paragraph'] is not None:
                dic['lead_paragraph'] = i['lead_paragraph']
            if i['snippet'] is not None:
                dic['snippet'] = i['snippet']
            filter_article_list.append(dic)

keys = filter_article_list[0].keys()
with open(r'articles_cleaned\atvi_articles\atvi_articles_cleaned.csv', 'w', newline='', encoding='utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(filter_article_list)

with open(r'articles_cleaned\atvi_articles\atvi_articles_cleaned.json', 'w') as fp:
    json.dump(filter_article_list, fp)
    

