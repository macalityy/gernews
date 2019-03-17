import tweepy
import pymongo
import json
from yaml import load


class FIMStreamListener(tweepy.StreamListener):

    def __init__(self, config):
        self.config = config

    def on_connect(self):
        print('Connecting to Twitter Streaming API...')

    def on_data(self, data):
        if self.config['output']['type'] == 'file':
            try:
                print(self.config['output']['file'])
                with open(self.config['output']['file'], 'a') as f:
                    f.write(data)
            except BaseException as e:
                print('Failed to write on_data %s' % str(e))

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            return False
