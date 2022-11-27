import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.markdown("# Time Filters")

st.markdown("""Use the Following Filters to display the most popular topics at a given point in 
            time leading up to the election. Date format is yyyy/mm/dd
            """)

start = st.date_input(
    "Start Date",
    min(st.session_state.data['date']),
    min_value = min(st.session_state.data['date']),
    max_value = max(st.session_state.data['date']))

end = st.date_input(
    "End Date",
    max(st.session_state.data['date']),
    min_value = min(st.session_state.data['date']),
    max_value = max(st.session_state.data['date']))

n_most = st.number_input('Number of Topics to display', value = 5, min_value = 1, max_value = 20)

if start and end and n_most:
    if start < end:
        time_period_df = st.session_state.data.loc[(st.session_state.data['date'] >= start) & (st.session_state.data['date'] <= end)]
        top_topics = time_period_df.groupby(['topic']).size().reset_index().sort_values(0, ascending = False)
        top_topics_list = top_topics[0:n_most]['topic']
        top_t_tweets = time_period_df.loc[time_period_df['topic'].isin(top_topics_list)]
        grouped_tweets = top_t_tweets.groupby(['topic','Name','date']).size().to_frame('size').reset_index()
        grouped_tweets['size_log'] = np.log(grouped_tweets['size'])
        fig = px.line(grouped_tweets, x = 'date', y = 'size_log', color = 'Name', hover_data=["size"],
                        labels={
                            "date": "Date",
                            "size_log": "Number of Tweets (log)",
                            "Name": "Topic Keywords",
                            "size": "Number of Tweets"
                        },
                        title="Time series of Consistently Popular Topics")
        st.plotly_chart(fig)

