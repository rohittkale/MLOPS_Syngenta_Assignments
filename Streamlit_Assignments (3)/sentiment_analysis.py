#Problem Statement 3: Create a Streamlit Application for Basic Sentiment Analysis
#Build a Streamlit application that takes user input in the form of text and performs basic sentiment analysis to determine whether the sentiment is positive, negative, or neutral.
#Create a github repository, push your code, experiment with using multiple branches, and then merge your changes into the main branch.
#Deploy your changes on Streamlit cloud

import streamlit as st
from textblob import TextBlob

st.title("Sentiment Analysis Application")

user_input = st.text_area("Enter text to analyze sentiment", "Type here...")

if st.button("Analyze"):
    if user_input:
        blob = TextBlob(user_input)
        sentiment_score = blob.sentiment.polarity

        if sentiment_score > 0:
            sentiment = "Positive"
        elif sentiment_score < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        st.write(f"Sentiment: {sentiment}")
        st.write(f"Sentiment Score: {sentiment_score}")
    else:
        st.warning("Please enter some text to analyze.")
