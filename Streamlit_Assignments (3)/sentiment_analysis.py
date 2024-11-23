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
