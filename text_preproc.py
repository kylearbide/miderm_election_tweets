import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import unidecode
import emoji
import spacy
import spacy_fastlang
from datetime import date
import re

today = date.today()

tweets = pd.read_excel("./data/data_tracker_final.xlsx")

tweets_clean = tweets.drop(['id', 'tweet_url', 'created_at', 'coordinates','media','urls','lang','place','possibly_sensitive','source','retweet_or_quote_user_id', 'retweet_or_quote_id', 'user_listed_count', 'user_name',
       'user_statuses_count', 'user_urls', 'retweet_count', 'user_created_at', 'in_reply_to_status_id', 'in_reply_to_user_id', 'in_reply_to_screen_name'], axis = 1)



tweets_clean['clean_text'] = tweets_clean['text'].apply(lambda x: emoji.demojize(x))
tweets_clean['clean_text'] = tweets_clean['clean_text'].apply(lambda x: unidecode.unidecode(x))
tweets_clean['clean_text'] = tweets_clean['clean_text'].apply(lambda x:re.sub(r'http\S+', '', x))
tweets_clean['mentions'] = tweets_clean['clean_text'].apply(lambda x: re.findall(r"@[a-zA-Z0-9_]*",x))
tweets_clean['clean_text'] = tweets_clean['clean_text'].apply(lambda x: re.sub(r"@[a-zA-Z0-9_]*","", x))
tweets_clean['clean_text'] = tweets_clean['clean_text'].apply(lambda x: re.sub(r":[a-zA-Z0-9_]*:","", x))
tweets_clean['clean_text'] = tweets_clean['clean_text'].apply(lambda x: re.sub(r"[^A-Za-z]+"," ", x))
tweets_clean = tweets_clean.loc[tweets_clean['clean_text'] != ""]
tweets_clean = tweets_clean.loc[tweets_clean['clean_text'].str.split().str.len() >= 10]

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe("language_detector")

tweets_clean['language_spacy'] = tweets_clean['clean_text'].apply(lambda x: nlp(x)._.language)
tweets_clean = tweets_clean.loc[tweets_clean['language_spacy'] == 'en']

tweets_clean.to_csv(f"./cleaned_data/{today}_clean.csv")

