1)run gather_tweet_dates_sentiments.py to gather all json files and sum up each individual sentiments for each dates and store into csv
- returns citi_senti_scores_for_all_dates.csv and sp_senti_scores_for_all_dates.csv
2)run both citi_assign_tweet_sentiment_scores.py & sp_assign_tweet_sentiment_scores.py
- generates C_Sentiment.csv and GSPC_Sentiment.csv
3)run assign_news_dates_sentiments.py 
- assigns news articles sentiments to C_Sentiment and GSPC_Sentiment
- generates C_Sentiment_Final.csv, GSPC_Sentiment_Final.csv
4)run stock_split_train_test.py to split C_Sentiment_Final.csv, and GSPC_Sentiment_Final.csv into train and test sets
- generates citi_train.csv, citi_test.csv, sp_train.csv, sp_test.csv
