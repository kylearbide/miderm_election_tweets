import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from ast import literal_eval

st.set_page_config(
    page_title="Midterm Election Tweets | Welcome",
    layout="wide"
)

st.session_state.data = pd.read_csv("./cleaned_data/final_topics_named.csv")

if not hasattr(st.session_state,"mention_data"):
    tweets = st.session_state.data
    tweets['mentions'] = tweets['mentions'].apply(lambda x: literal_eval(x))
    st.session_state.mention_data = tweets.explode('mentions')

st.title("Exploring Election Discussion on Twitter")
st.markdown("""Welcome to this tool for exporing tweets collected during and about the 2022 Midterm Elections.
                This app will allow you to filter and vizualize from our dataset of tweets which have been mapped
                to topics using BERTopic. A link to our full report can be found [here] where you can find our discussion
                of analysis and methods. Feel free to check out our source code located [here]""")

st.header("Exploratory Analysis")
st.markdown("""During our analysis, we discovered some trends and were able to distinguish between two
types of topics: continuous and event based. Continuous topics are consistently prevelant in the data and typically
increase in frequency along with the frequency of total tweets. A timeseries representation of this type of topic will
look something like this:
""")

top_topics = st.session_state.data.groupby(['topic']).size().reset_index().sort_values(0, ascending = False)
top_topics_list = top_topics[1:7]['topic']
top_t_tweets = st.session_state.data.loc[st.session_state.data['topic'].isin(top_topics_list)]
top_t_tweets['date'] = pd.to_datetime(top_t_tweets['parsed_created_at']).dt.date
grouped_tweets = top_t_tweets.groupby(['topic','Name','date']).size().to_frame('size').reset_index()
simple_grouped_tweets = grouped_tweets.loc[grouped_tweets['topic'] != 71]
simple_grouped_tweets['size_log'] = np.log(simple_grouped_tweets['size'])
fig = px.line(simple_grouped_tweets, x = 'date', y = 'size_log', color = 'Name', hover_data=["size"],
                labels={
                     "date": "Date",
                     "size_log": "Number of Tweets (log)",
                     "Name": "Topic Keywords",
                     "size": "Number of Tweets"
                 },
                title="Time series of Consistently Popular Topics")
st.plotly_chart(fig)

st.markdown("""Event based topics see large spikes in frequecy at certain times but generally are discussed
fairly infrequently. We theorize that this is occurs when topics are coorelated with real like events, but this
could happen for a number of reasons (ex. bot spamming). The timeseries representation of this type of topic looks something
like this:
""")

st.session_state.data['date'] = pd.to_datetime(st.session_state.data['parsed_created_at']).dt.date
top_v_tweets = st.session_state.data.loc[st.session_state.data['topic'].isin([51,61,71])]
grouped_tweets = top_v_tweets.groupby(['topic','Name','date']).size().to_frame('size').reset_index()
grouped_tweets['size_log'] = np.log(grouped_tweets['size'])
fig = px.line(grouped_tweets, x = 'date', y = 'size_log', color = 'Name', hover_data=["size"],
                labels={
                     "date": "Date",
                     "size_log": "Number of Tweets (log)",
                     "Name": "Topic Keywords",
                     "size": "Number of Tweets"
                 },
                title="Time series of Event Based Topics")
st.plotly_chart(fig)
