import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import re
from collections import Counter
from wordcloud import WordCloud

# Load dataset
@st.cache_data
def load_data():
    file_path = "footway_cs_dataset.json"
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

df = load_data()

# Convert timestamp to datetime and extract relevant information
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["date"] = df["timestamp"].dt.date
df["hour"] = df["timestamp"].dt.hour
df["email_length"] = df["incomingEmail"].dropna().apply(len)

# Sidebar filters
st.sidebar.header("Filters")
category_filter = st.sidebar.multiselect("Select Category", df["category"].unique())
language_filter = st.sidebar.multiselect("Select Language", df["detectedLanguage"].unique())

filtered_df = df.copy()
if category_filter:
    filtered_df = filtered_df[filtered_df["category"].isin(category_filter)]
if language_filter:
    filtered_df = filtered_df[filtered_df["detectedLanguage"].isin(language_filter)]

# Title
st.title("Customer Service Dashboard")

# Category Distribution
st.subheader("Category Distribution")
fig, ax = plt.subplots()
df["category"].value_counts().plot(kind="bar", ax=ax, color='blue')
plt.xticks(rotation=45, ha="right")
st.pyplot(fig)

# Language Distribution
st.subheader("Language Distribution")
fig, ax = plt.subplots()
df["detectedLanguage"].value_counts().plot(kind="bar", ax=ax, color='cyan')
st.pyplot(fig)

# Inquiry Trends Over Time
st.subheader("Inquiry Trends Over Time")
daily_counts = df.groupby("date").size()
fig, ax = plt.subplots(figsize=(10, 5))
daily_counts.plot(kind="bar", ax=ax)
ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Number of Inquiries", fontsize=12)
ax.set_title("Inquiry Trends Over Time", fontsize=14)
ax.set_xticklabels(daily_counts.index.astype(str), rotation=90)
st.pyplot(fig)

# Peak Inquiry Hours Analysis
st.subheader("Peak Inquiry Hours")
fig, ax = plt.subplots()
df["hour"].value_counts().sort_index().plot(kind="bar", ax=ax, color='purple')
ax.set_xlabel("Hour of the Day")
ax.set_ylabel("Number of Inquiries")
ax.set_title("Peak Inquiry Hours")
st.pyplot(fig)

# Most Common Words in Emails
st.subheader("Most Common Words in Emails")
text_data = " ".join(df["incomingEmail"].dropna())
words = re.findall(r'\b\w+\b', text_data.lower())
word_counts = Counter(words)
most_common_words = word_counts.most_common(20)
common_words_df = pd.DataFrame(most_common_words, columns=["Word", "Frequency"])
st.write(common_words_df)

# Keyword Trend Over Time
st.subheader("Keyword Trend Over Time")
keyword = st.text_input("Enter a keyword to analyze over time")
if keyword:
    df["keyword_present"] = df["incomingEmail"].dropna().apply(lambda x: keyword.lower() in x.lower())
    keyword_trend = df.groupby("date")["keyword_present"].sum()
    fig, ax = plt.subplots()
    keyword_trend.plot(kind="bar", ax=ax, color='orange')
    ax.set_xlabel("Date")
    ax.set_ylabel(f"Occurrences of '{keyword}'")
    ax.set_title(f"Trend of '{keyword}' Over Time")
    st.pyplot(fig)

# Email Length Analysis
st.subheader("Email Length Distribution")
fig, ax = plt.subplots()
sns.histplot(df["email_length"], bins=30, kde=True, ax=ax)
ax.set_xlabel("Email Length (characters)")
ax.set_title("Distribution of Email Lengths")
st.pyplot(fig)

# Sentiment Analysis with User Input
st.subheader("Customize Sentiment Words")

default_good_words = {"excellent", "great", "good", "amazing", "satisfied", "happy", "love", "wonderful", "best", "perfect"}
default_bad_words = {"bad", "poor", "worst", "awful", "terrible", "unsatisfied", "angry", "horrible", "disappointed", "problem"}

# Allow user to modify words
user_good_words = st.text_area("Enter positive words (comma separated)", ", ".join(default_good_words))
user_bad_words = st.text_area("Enter negative words (comma separated)", ", ".join(default_bad_words))

# Convert user input to sets
good_words = set(map(str.strip, user_good_words.split(","))) if user_good_words else default_good_words
bad_words = set(map(str.strip, user_bad_words.split(","))) if user_bad_words else default_bad_words

def classify_feedback(text):
    words = set(re.findall(r'\b\w+\b', text.lower()))
    good_count = len(words & good_words)
    bad_count = len(words & bad_words)

    if good_count > bad_count:
        return "Positive"
    elif bad_count > good_count:
        return "Negative"
    else:
        return "Neutral"

df["feedback_sentiment"] = df["incomingEmail"].dropna().apply(classify_feedback)

# Display sentiment analysis results
st.subheader("Customer Feedback Sentiment Analysis")
sentiment_counts = df["feedback_sentiment"].value_counts()
fig, ax = plt.subplots()
sentiment_counts.plot(kind="bar", ax=ax, color=['green', 'red', 'gray'])
plt.xticks(rotation=0)
st.pyplot(fig)

# Search Functionality
st.subheader("Search Emails")
search_query = st.text_input("Enter search keyword")
if search_query:
    search_results = filtered_df[filtered_df["incomingEmail"].str.contains(search_query, case=False, na=False)]
    st.write(search_results[["timestamp", "incomingEmail", "category"]])
