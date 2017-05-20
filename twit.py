import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener #Streams connection
import time
import argparse
import string
import config
import json
from nltk.tokenize import word_tokenize
import re
import operator
from collections import Counter
from nltk.corpus import stopwords

consumer_key = 'LnZwqXojPjni4BMmm6dk3eIRu'
consumer_secret = 'ERpqOOHp2px4r3VRiqSXP8IZwrkPFlArWQvsAKM9o1x78JSI6A'
access_token = '827568847-wm5zbFSLUUpYrWwnLwqOznCcOs1wajCFadT8oc1u'
access_secret = 'O4RWFvomufTxAc7oF3ykR4cg0Q2BEP5YDM3tUb7tQjjIx'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

def process_or_store(tweet):
    with open('data.txt', 'w') as out:
        json.dumps(tweet, out)

## list of all tweets
# REMEMBER error code 429 is for too many requests
for status in tweepy.Cursor(api.home_timeline).items(10):
    process_or_store(status._json)

""" for friend in tweepy.Cursor(api.friends).items():
    process_or_store(friend._json) """

""" for tweet in tweepy.Cursor(api.user_timeline).items():
    process_or_store(tweet._json) """

class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('NBA.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#NBA'])



#Test
# tweet1 = 'RT @johnnymedhanie: test 1 www.google.ca #CODE '
# print (word_tokenize(tweet1))

emoticons_str = r"""
(?:
    [:=;] # these are eyes
    [oO\-]? # noses
    [D\)\]\(\]/\\OpP] # mouths ##possible area of going wrong. Check.
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', #HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', ##numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

token_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens ]
    return tokens

#tryout
test1 = 'RT @johnnymedhanie: alpha bravo charlie www.johnnymedhanie.github.io #Nice'
print(preprocess(test1))


### COMMON WORDS?
punctuation - list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']
terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]

fname = 'NBA.json'
with open(fname, 'a') as f:
    count_all = Counter()
    for line in f:
        tweet = json.loads(line)
        terms_all = [term for term in preprocess(tweet['text'])]
        json.dump(count_all.update(terms_all), fname)
