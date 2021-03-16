import streamlit as st
import pandas as pd
import numpy as np

st.title("Airline Sentiment Analysis")
st.sidebar.title("Sentiment Analysis of Tweets about Airlines")

st.markdown("This application is a Streamlit dashboard to analyze the sentiment of Tweets about US airlines")
st.sidebar.markdown("This application is a Streamlit dashboard to analyze the sentiment of Tweets about US airlines")

DATA_URL = "Tweets.csv"


@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data["tweet_created"] = pd.to_datetime(data["tweet_created"])
    return data


data = load_data()

st.sidebar.subheader("Show random Tweet")
random_tweet = st.sidebar.radio("Sentiment", ("positive", "neutral", "negative"))
st.sidebar.markdown(data.query("airline_sentiment == @random_tweet")[["text"]].sample(n=1).iat[0, 0])
