bert_sentiment_analyzer.py is the script to assign sentiment scores the preprocessed tweets.
- takes long time (5 tweets scored per second)
sentiment scoring can be performed on google collab using GPU for faster timing.
- upload bert_sentiment_analyzer.ipynb to google collaboratory and enable GPU in the runtime

assign_neutral_sentiment.py assigns a tweet neutral (0) sentiment if
(confidence 2 minus confidence 1) is within the range of -0.3 to 0.3
confidence 2 // positive confidence level
confidence 1 // negative confidence level