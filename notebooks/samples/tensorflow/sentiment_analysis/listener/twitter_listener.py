# Copyright 2020 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Collects tweets using hashtags."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import datetime
import json
import logging
import sys
from tenacity import retry, retry_if_exception_type, stop_after_attempt, \
    wait_exponential
import time
import urllib3

import tweepy
from tweepy.streaming import StreamListener

from config import get_authentication
from config import get_publisher
from config import get_topic

logger = logging.getLogger()

_HASH_TAGS = ['#covid19']
_RATE_LIMIT_RETRIES = 3
_RETRY_DELAY = 1
_RETRY_MULTIPLIER = 1
_RETRY_MAX_DELAY = 4
# Timestamp format for tweet
_TIME_FORMAT = '%a %b %d %H:%M:%S +0000 %Y'
_CREATED_FORMAT = '%Y-%m-%d %H:%M:%S'

_TWEET_FIELDS = ['text', 'user_id', 'id', 'favorite_count', 'retweet_count',
                 'media', 'posted_at']
_PROCESSED_TWEET_FIELDS = ['id', 'lang', 'retweeted_id', 'favorite_count',
                          'retweet_count', 'coordinates_latitude',
                          'coordinates_longitude', 'place', 'user_id',
                          'created_at', 'hashtags', 'user_mentions', 'text',
                          'media']

Tweet = collections.namedtuple('Tweet', _TWEET_FIELDS)
ProcessedTweet = collections.namedtuple('ProcessedTweet',
                                        _PROCESSED_TWEET_FIELDS)

publisher = get_publisher()
topic_path = get_topic(publisher)


# Custom listener class
class Listener(StreamListener):
    """A listener handles tweets that are received from the stream.
    This is a basic listener that pushes tweets to Google Cloud PubSub.
    """

    def __init__(self):
        super(Listener, self).__init__()

    def on_status(self, status):
        write_to_pubsub(reformat_tweet(status._json))
        return True

    def on_error(self, status_code):
        logging.error('Error with status code:', status_code, sys.stderr)
        if status_code == 420:
            logging.error('Rate limit active')
            return False


# Method to push messages to pubsub
def write_to_pubsub(data):
    """

    :param data:
    :return:
    """
    try:

        posted_at = datetime.datetime.fromtimestamp(
            data['created_at']).strftime(_CREATED_FORMAT)
        tweet = Tweet(data['text'], data['user_id'], data['id'],
                      data['favorite_count'], data['retweet_count'],
                      ','.join(map(str, data['media'])), posted_at)
        tweet_data = json.dumps(tweet._asdict()).encode('utf-8')
        if data['lang'] == 'en':
            publisher.publish(topic_path,
                              data=tweet_data,
                              tweet_id=str(data['id']).encode('utf-8'))
    except Exception as e:
        raise e


# Method to format a tweet from tweepy.
def reformat_tweet(tweet):
    """

    :param tweet:
    :return:
    """
    hashtags = []
    media = []
    user_mentions = []

    # Extract Tweet information.
    entities = tweet.get('entities')
    extended_entities = tweet.get('extended_entities')

    if entities.get('hashtags'):
        hashtags = [
            {'text': y['text'], 'startindex': y['indices'][0]} for y in
            entities.get('hashtags')]

    if entities.get('user_mentions'):
        user_mentions = [
            {'screen_name': y['screen_name'], 'startindex': y['indices'][0]}
            for y in entities.get('user_mentions')]

    # Media URL
    if extended_entities:
        if extended_entities.get('media'):
            media = [
                {'media_url': y['media_url'],
                 'media_url_https': y['media_url_https']} for y in
                extended_entities.get('media')]

    # Extract Text.
    if 'extended_tweet' in tweet:
        text = tweet['extended_tweet'].get('full_text')
    elif 'full_text' in tweet:
        text = tweet.get('full_text')
    else:
        text = tweet.get('text')

    processed_tweet = ProcessedTweet(id=tweet['id'],
                                     lang=tweet['lang'],
                                     retweeted_id=tweet['retweeted_status'][
                                         'id'] if 'retweeted_status' in tweet
                                     else None,
                                     favorite_count=tweet[
                                         'favorite_count'] if
                                     'favorite_count' in tweet else 0,
                                     retweet_count=tweet[
                                         'retweet_count'] if 'retweet_count'
                                                             in tweet else 0,
                                     coordinates_latitude=
                                     tweet['coordinates']['coordinates'][0] if
                                     tweet['coordinates'] else 0,
                                     coordinates_longitude=
                                     tweet['coordinates']['coordinates'][0] if
                                     tweet['coordinates'] else 0,
                                     place=tweet['place']['country_code'] if
                                     tweet['place'] else None,
                                     user_id=tweet['user']['id'],
                                     created_at=time.mktime(
                                         time.strptime(tweet['created_at'],
                                                       _TIME_FORMAT)),
                                     hashtags=hashtags,
                                     user_mentions=user_mentions,
                                     text=text,
                                     media=media)
    logging.info(processed_tweet._asdict())
    return processed_tweet._asdict()


@retry(retry=retry_if_exception_type(urllib3.exceptions.ReadTimeoutError),
       stop=stop_after_attempt(_RATE_LIMIT_RETRIES),
       wait=wait_exponential(multiplier=_RETRY_MULTIPLIER,
                             min=_RETRY_DELAY,
                             max=_RETRY_MAX_DELAY),
       reraise=True,)
def start_stream(stream, **kwargs):
    """

    :param stream:
    :param kwargs:
    :return:
    """
    try:
        stream.filter(**kwargs)
    except urllib3.exceptions.ReadTimeoutError:
        stream.disconnect()
        logging.exception('ReadTimeoutError Exception')


def main():
    auth = get_authentication()
    twitter_stream = tweepy.Stream(auth,
                                   listener=Listener(),
                                   tweet_mode='extended')
    try:
        logging.info('Start Twitter streaming...')
        start_stream(twitter_stream, track=_HASH_TAGS)
    except KeyboardInterrupt:
        logging.exception('Stopped.')
    finally:
        logging.info('Done.')
        twitter_stream.disconnect()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
