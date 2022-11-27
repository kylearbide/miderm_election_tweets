import numpy as np
from bertopic import BERTopic
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
np.random.seed(2018)

"""
The purpose of this script is to apply the topics from the trained topic model to all our tweets. This
takes some time so its best done in batches
"""

stop = stopwords.words('english')
stop.extend(['election','vote','midterms','midterm','elect','elections', 'senate', 'house',"us","democracy", "amp", "midtermelections"])

tweets = pd.read_csv("./cleaned_data/2022-11-23_clean.csv")
tweets['date'] = pd.to_datetime(tweets['parsed_created_at'])
tweets = tweets.loc[(tweets['date'] > "2022-11-07")&(tweets['date'] <= "2022-11-11")]

tweets['clean_text'] = tweets['clean_text'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
tweets = tweets.loc[tweets['clean_text'].str.split().str.len() >= 10].reset_index()

topic_model = BERTopic.load("./models/model_bert")

topics, probs = topic_model.transform(tweets['clean_text'])
tweets['topic'] = topics
tweets['model'] = 1

tweets.to_csv(f"./cleaned_data/final_w_topics_3.csv")






