## Import standard packages
import datetime
import json
import re

## Import tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

## Import our Credentials
CREDENTIALS = json.loads(open('creds.json', 'r').read())

def make_fixed_length(text, desired_len):
    """
    Takes a length of text and either cuts it down to
    size or adds a space buffer to the end of it.
    """
    if len(text) == desired_len:
        return text
    if len(text) > desired_len:
        return text[0:desired_len]
    if len(text) < desired_len:
        x = len(text)
        while x < desired_len:
            text = text + ' '
            x+=1
        return text

def pretty_print_tweet(tweet):
    # Get account name, tweet
    account_name = tweet['user']['screen_name']
    tweet_text = tweet['text']

    # Clean up the tweet text to remove emoji and garbage
    tweet_text = re.sub(r'([^\s\w]|_)|\n|\r', '', tweet_text)

    # Print it nicely
    print(datetime.datetime.now().strftime("%H:%M:%S") + ' | @' + make_fixed_length(account_name, 9) + ' | ' + make_fixed_length(tweet_text, 100))

class StdOutListener(StreamListener):
    def __init__(self):
        pass

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            pretty_print_tweet(tweet)
        except:
            pass
        return True

    def on_error(self, status):
        print(status)

class Twitter:
    def __init__(self):
        self.listener = StdOutListener()
        self.auth = OAuthHandler(CREDENTIALS['c_key'], CREDENTIALS['c_secret'])
        self.auth.set_access_token(CREDENTIALS['a_token'], CREDENTIALS['a_token_secret'])

    def print_live_stream(self, terms):
        stream = Stream(self.auth, self.listener)
        stream.filter(track=terms)

if __name__ == '__main__':
    streamer = Twitter()
    streamer.print_live_stream(CREDENTIALS['topics'])
