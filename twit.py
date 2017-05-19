import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener #Streams connection
import time
import argparse
import string
# import config
import json
from nltk.tokenize import word_tokenize
import re

consumer_key = 'LnZwqXojPjni4BMmm6dk3eIRu'
consumer_secret = 'ERpqOOHp2px4r3VRiqSXP8IZwrkPFlArWQvsAKM9o1x78JSI6A'
access_token = '827568847-wm5zbFSLUUpYrWwnLwqOznCcOs1wajCFadT8oc1u'
access_secret = 'O4RWFvomufTxAc7oF3ykR4cg0Q2BEP5YDM3tUb7tQjjIx'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

def process_or_store(tweet):
    print(json.dumps(tweet))

## list of all tweets
# error code 429 is for too many requests
for status in tweepy.Cursor(api.home_timeline).items(10):
    process_or_store(status._json)

""" for friend in tweepy.Cursor(api.friends).items():
    process_or_store(friend._json) """

""" for tweet in tweepy.Cursor(api.user_timeline).items():
    process_or_store(tweet._json) """

def get_parser():
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q", "--query", dest="query", help="Query/Filter", default="-")
    parse.add_argument("-d","--data-dir", dest="data_dir", help="Output/Data Directory")
    return parser

#streaming
class MyListener(StreamListener):
    def __init__(self, data_dir, query):
        query_fname = format_filename(query)
        self.outfile = "%s/stream_%s.json" % (data_dir, query_fname)

    def on_data(self, data):
        try:
            with open('NBA.json', 'a') as f:
                f.write(data)
                print(data)
                return True
        except BaseException as e:
                print("Error on_data: %s" % str(e))
                time.sleep(5)
        return True

    def on_error(self, status):
                    print(status)
                    return True

    def format_filename(fname):  # time to change fname into a string
        return ''.join(convert_valid(one_char) for one_char in fname)

    def convert_valid(one_char):
        valid_chars ="-_.%s%s" % (string.ascii_letters, string.digits)
        if one_char in valid_chars:
            return one_char
        else:
            return '_'

    @classmethod
    def parse(cls, api, raw):
        status = cls.first_parse(api, raw)
        setattr(status, 'json'. json.dumps(raw))
        return status

    if __name__ == '__main__':
        parser = get_parser()
        args = parser.parse.args()
        auth = OAuthHandler(config.consumer_key, config.consumer_secret)
        auth.set_access_token(config.access_token, config.access_secret)
        api = tweepy.API(auth)


twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=["NBA"])



#Test
tweet1 = 'RT @johnnymedhanie: test 1 www.google.ca #CODE '
print (word_tokenize(tweet1))

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
