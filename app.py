import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("Airline Sentiment Analysis")
st.sidebar.title("Sentiment Analysis of Tweets about Airlines")

st.sidebar.markdown("This application is a Streamlit dashboard that analyzes the sentiment of Tweets about US airlines")

DATA_URL = "Tweets.csv"


@st.cache(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data["tweet_created"] = pd.to_datetime(data["tweet_created"])
    return data


data = load_data()

st.sidebar.subheader("Show random Tweet")
random_tweet = st.sidebar.radio("Sentiment:", ("positive", "neutral", "negative"))
st.sidebar.markdown(data.query("airline_sentiment == @random_tweet")[["text"]].sample(n=1).iat[0, 0])

st.sidebar.markdown("### Number of Tweets by sentiment")
select = st.sidebar.selectbox("Visualization type:", ["Histogram", "Pie Chart"], key="1")
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({"Sentiment": sentiment_count.index, "Tweets": sentiment_count.values})

if not st.sidebar.checkbox("Toggle Display", True):
    st.markdown("### Number of Tweets by sentiment")
    if select == "Histogram":
        fig = px.bar(sentiment_count, x="Sentiment", y="Tweets", color="Tweets", height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values="Tweets", names="Sentiment")
        st.plotly_chart(fig)

st.sidebar.subheader("When and where are users tweeting from?")
hour = st.sidebar.slider("Hour of day", 0, 23)
modified_data = data[data["tweet_created"].dt.hour == hour]
if not st.sidebar.checkbox("Toggle Display", True, key="1"):
    st.markdown("### Tweets locations based on the time of day")
    st.markdown("%i Tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour + 1) % 24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

st.sidebar.subheader("Breakdown of airline tweets by sentiment")
choice = st.sidebar.multiselect("Pick airline:", ("US Airways", "United", "American", "Southwest", "Delta", "Virgin America"),
                                key=0)

if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data, x="airline", y="airline_sentiment", histfunc="count",
                              color="airline_sentiment",
                              facet_col="airline_sentiment", labels={"airline_sentiment": "tweets"}, height=600,
                              width=800)
    st.plotly_chart(fig_choice)

st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio("Display Word Cloud for which sentiment?", ("positive", "neutral", "negative"))

if not st.sidebar.checkbox("Toggle Display", True, key="3"):
    st.header("Word Cloud for %s sentiment" % word_sentiment)
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ' '.join(df["text"])
    processed_words = ' '.join([word for word in words.split() if "http" not in word and not word.startswith('@')
                                and word != "RT"])
    word_cloud = WordCloud(stopwords=STOPWORDS, background_color="white", height=640,
                           width=800).generate(processed_words)
    plt.imshow(word_cloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot(plt)
