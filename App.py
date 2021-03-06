import streamlit as st
import pandas as pd
from visualize import *
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
import string
from textblob import TextBlob

punc = string.punctuation
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


st.title("SENTIMENT ANALYSIS")
sidebar = st.sidebar
st.image("abc.jpg")
st.text("Sentiment analysis refers to identifying as well as classifying the sentiments that are expressed in the text source. Tweets are often useful in generating a vast amount of sentiment data upon analysis.")
sidebar = st.sidebar
sidebar.title("sidebar title")
choice_list = ["View_DataSet", "View Sentiment Analysis", "EDA"]
choice = sidebar.selectbox("Select Option", choice_list)

df = pd.read_csv("dataset/covid19_tweets.csv").head(1000)


def View_DataSet():
    st.markdown("""
       ## NAME
       **Anurag Pathak**
    """)


@st.cache()
def clean_text(text):
    '''Make text lowercase, remove text in square brackets,remove links,remove punctuation
    and remove words containing numbers.'''

    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)

    # Removing stopwords
    text = " ".join([word for word in str(
        text).split() if word not in stop_words])

    # Stemming
    text = " ".join([stemmer.stem(word) for word in text.split()])

    # Lemmatization
    text = " ".join([lemmatizer.lemmatize(word) for word in text.split()])

    return text


@st.cache()
def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def analyseSentiment():
    st.header('detail')

    df['text'] = df['text'].apply(lambda x: remove_emoji(x))

    df['text'] = df['text'].apply(lambda x: clean_text(x))
    sentiments = []
    subjectivity = []
    for tweet in df['text'].values:
        blob = TextBlob(tweet)
        senti = blob.sentiment.polarity
        if senti > 0:
            sentiments.append('positive')
        elif senti < 0:
            sentiments.append('negative')
        else:
            sentiments.append('neutral')
        subjectivity.append(blob.sentiment.subjectivity)

    df['sentiment'] = sentiments
    df['subjectivity'] = subjectivity

    data = df.groupby('sentiment').count().reset_index()
    st.dataframe(df)
    st.plotly_chart(plotPie(data=data, values='text',
                            names='sentiment', title='title'), use_container_width=True)
    st.plotly_chart(plotBar(data=data, x='text', y='sentiment',
                            title='title'), use_container_width=True)

    st.plotly_chart(plotHistogram(data=data, x="subjectivity",
                                  title='title'), use_container_width=True)


def analyseEDA():
    st.header('Exploratoy Data Analysis')

    data = df.groupby('user_location').count().reset_index().sort_values(
        'user_name', ascending=False).head(10)
    st.plotly_chart(plotBar(data, 'user_location', 'date',
                            'title'), use_container_width=True)

    data = df.groupby('source').count().reset_index().sort_values(
        'user_name', ascending=False).head(10)
    st.dataframe(data)
    st.plotly_chart(plotPie(data, 'source', 'date',
                            'title'), use_container_width=True)

    st.dataframe(df.groupby('user_verified').count().reset_index())

    st.plotly_chart(plotPie(df.groupby('user_verified').count(
    ).reset_index(), 'user_verified', 'user_name', 'title'), use_container_width=True)
    st.plotly_chart(plotHistogram(df, 'user_followers',
                                  'title'), use_container_width=True)


    data["date"] = pd.to_datetime(data["date"])
    data["Month"] = data["date"].apply(lambda x : x.month)
    data["day"] = data["date"].apply(lambda x : x.dayofweek)
    dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
    data["day"] = data["day"].map(dmap)

    st.plotly_chart()


if choice == choice_list[0]:
    View_DataSet()
elif choice == choice_list[1]:
    analyseSentiment()
elif choice == choice_list[2]:
    analyseEDA()
