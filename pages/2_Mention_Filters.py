import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from ast import literal_eval

st.markdown("# Filter by Mentions")

st.markdown("""This page allows you to filter for tweets were a specified user is mentioned. The purpose here is
            to allow you understand what topics are being discussed in coorelation with specific people or media group.
            Need some inspiration? Try search for one of the most popular users show below...
            """)

if not hasattr(st.session_state,"mention_data"):
    tweets = st.session_state.data
    tweets['mentions'] = tweets['mentions'].apply(lambda x: literal_eval(x))
    st.session_state.mention_data = tweets.explode('mentions')
grouped_mentions = st.session_state.mention_data.groupby(['mentions']).size().to_frame('size').reset_index().sort_values("size", ascending = False)

fig = px.bar(grouped_mentions[0:10], y = 'mentions', x = 'size', orientation='h',
                labels={
                     "size": "Number of Mentions",
                     "mentions": "User Screen Name"
                 },
                title="Top Mentioned Users")
st.plotly_chart(fig)

st.markdown("Type the name screen name of the user, starting with '@'")

user_screen_name = st.text_input("Screen Name")

if user_screen_name:
    user_tweets = st.session_state.mention_data.loc[st.session_state.mention_data['mentions'] == user_screen_name]
    if not user_tweets.empty:
        top_topics = user_tweets.groupby(['topic']).size().to_frame('size').reset_index().sort_values('size', ascending = False)
        top_topics_list = top_topics[0:7]['topic']
        top_t_tweets = user_tweets.loc[user_tweets['topic'].isin(top_topics_list)]
        grouped_tweets = top_t_tweets.groupby(['topic','Name','date']).size().to_frame('size').reset_index()
        grouped_tweets['size_log'] = np.log(grouped_tweets['size'])
        fig = px.line(grouped_tweets, x = 'date', y = 'size_log', color = 'Name',hover_data=["size"],
                        labels={
                            "date": "Date",
                            "size_log": "Number of Tweets (log)",
                            "Name": "Topic Keywords",
                            "size": "Number of Tweets"
                        },
                        title=f"Time series of Top Topics Mentioning {user_screen_name}")
        st.plotly_chart(fig)

        top_topics = user_tweets.groupby(['topic','Name']).size().to_frame('size').reset_index().sort_values('size', ascending = False)
        top_topics['size_log'] = np.log(top_topics['size'])
        fig = px.bar(top_topics[0:7], y = 'Name', x = 'size_log', orientation='h', hover_data = ['size'],
                    labels={
                            "size": "Number of Tweets",
                            "Name": "Topic Keywords",
                            "size_log": "Number of Tweets (log)"
                        },
                        title=f"Time series of Top Topics Mentioning {user_screen_name}")
        # fig.update_xaxes(
        #         tickangle = 45,
        #         title_text = "Topic")
        st.plotly_chart(fig)

        st.markdown("### View example tweets by topic for this user")

        option = st.selectbox("Select Topic", list(top_t_tweets['Name'].unique()))

        if option:
            st.write(top_t_tweets.loc[top_t_tweets['Name'] == option]['text'].iloc[0])
            st.write(top_t_tweets.loc[top_t_tweets['Name'] == option]['text'].iloc[1])
            st.write(top_t_tweets.loc[top_t_tweets['Name'] == option]['text'].iloc[2])
    else:
        st.error("Please enter a valid screen name")


