import tweepy
from tweepy import OAuthHandler, Stream, StreamListener
import time
import argparse
import string
import json
import config

consumer_key = 'N'
consumer_secret = 'O'
access_token = 'P'
access_secret = 'E'


def get_parser():
    parser = argparse.ArgumentParser(description="NBA twitter stream downloader")
    parser.add_argument("-q", "--query", dest="query", help="Query/Filter", default='-')
    parser.add_argument("-d", "--data-dir", dest="data-dir", help="Output/Data Directory")
    return parser


def process_or_store(tweet):
    with open('data.txt, w') as out:
        json.dumps(tweet, out)

class MyListener(StreamListener):
    def __init__(self, data_dir, query):
        query_fname = format_filename
        self.outfile = "%s/stream_%s".json % (data_dir, query_fname)
    def on_data(self, data):
        try:
            with open('base.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
                print("Error: on_data %s" % str(e))
                time.sleep(5)
        return True

    def on_error(self, status):
            print(status)
            return True
def format_filename(fname):
    return ''.join(convert_valid(one_char) for one_char in fname)

def convert_valid(one_char):
    valid_chars = "-_%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

if __name__ = '__main__':
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler(config.consumer_key, config)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)

twitter_stream = Stream(auth, MyListener(args.data_dir, args.query))
twitter_stream.filter(track=[args.query])
