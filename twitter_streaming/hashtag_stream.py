import os
import sys
import getopt
import tweepy
from listener import FIMStreamListener
from yaml import safe_load


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'hc:', ['config'])
    except getopt.GetoptError:
        print('hashtag_stream.py -c <config>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == 'h':
            print('hashtag_stream.py -c <config>')
            sys.exit()
        if opt in ('-c', '--config'):
            config = safe_load(open(arg))

    if not opts:
        print('No config file specified')
        print('hashtag_stream.py -c <config>')
        sys.exit(2)

    auth = tweepy.OAuthHandler(
        config['twitter']['consumer-key'], config['twitter']['consumer-secret'])
    auth.set_access_token(
        config['twitter']['access-key'], config['twitter']['access-secret'])

    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    mongo_stream = tweepy.Stream(
        auth=api.auth, listener=FIMStreamListener(config))

    print('Streaming hashtags:')
    [print('> {}'.format(h)) for h in config['stream']['hashtag']]

    mongo_stream.filter(track=config['stream']['hashtag'])


if __name__ == '__main__':
    main(sys.argv[1:])
