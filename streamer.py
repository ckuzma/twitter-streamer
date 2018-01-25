## Import standard packages
import json
import re

## Import tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream

## Import our Credentials
CREDENTIALS = json.loads(open('creds.json', 'r').read())

def pretty_print_tweet(tweet):
    tweet['text'] = re.sub(r'([^\s\w]|_)|\n|\r', '', tweet['text'])
    print(tweet['text'] + '\t(@' + tweet['user']['screen_name'] + ')')

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        tweet = json.loads(data)
        try:
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
    streamer.print_live_stream(['alexa', 'echo'])
