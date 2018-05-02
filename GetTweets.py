import tweepy
from tweepy import OAuthHandler
import json
import re

def get_tweets(topic, n):

    # Authentication
    c_key = '7FjEPU3ngM9ekufFwRM9XPy0F'
    c_secret = 'db1GpaYG4TfIJNvBcZFzfPourLQv1SDcghFr1JRZMHBYRp1TQa'
    a_token = '777643491031560192-F6iIrQrWZJQ81E14q6fsJmXs11rQFZ3'
    a_secret = 'qZl60WChgsR5EYmjbIV2waQBElNHryWp6424OgT2nLPVL'

    auth = OAuthHandler(c_key, c_secret)
    auth.set_access_token(a_token, a_secret)
    api = tweepy.API(auth)

    # Get the most recent 3000 tweets for this topic
    tweets = []
    for tweet in tweepy.Cursor(api.search, q=topic, lang='en').items(n):
        tweets.append(tweet)
    return tweets

def get_text(tweets):
    tweet_texts = []
    for tweet in tweets:
        tweet = re.sub(r"http\S+", "", tweet.text)
        tweet = re.sub(r"@\S+", "", tweet)
        tweet = re.sub(r"RT ", "", tweet)
        tweet_texts.append(tweet)
    return tweet_texts
