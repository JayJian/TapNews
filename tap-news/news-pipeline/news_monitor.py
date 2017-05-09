# -*- coding: utf-8 -*-
import datetime
import hashlib
import os
import sys
import redis

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import news_api_client
# import CloudAMQPClient class from cloudAMQP_client.py
from cloudAMQP_client import CloudAMQPClient
import yaml

with open('../config.yaml', 'r') as configFile:
    cfg = yaml.load(configFile)

DEDUPE_NEWS_TASK_QUEUE_URL = cfg['cloudAMQP']['dedupe_news_task_queue_url']
DEDUPE_NEWS_TASK_QUEUE_NAME = cfg['cloudAMQP']['dedupe_news_task_queue_name']
SCRAPE_NEWS_TASK_QUEUE_URL = cfg['cloudAMQP']['scrape_news_task_queue_url']
SCRAPE_NEWS_TASK_QUEUE_NAME = cfg['cloudAMQP']['scrape_news_task_queue_name']

REDIS_HOST = cfg['redis']['host']
REDIS_PORT = cfg['redis']['port']

NEWS_TIME_OUT_IN_SECONDS = 3600 * 24
SLEEP_TIME_IN_SECONDS = 10

NEWS_SOURCE = [
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'ign',
    'new-scientist',
    'techcrunch',
    'techradar',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post',
    'usa-today'
]

# initialize redis client and cloudAMQP client
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

while True:
    news_list = news_api_client.getNewsFromSource(NEWS_SOURCE)

    #keep track of how many new news we get
    num_of_new_news = 0

    for news in news_list:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

        # check whether it is a new news
        if redis_client.get(news_digest) is None:
            num_of_new_news = num_of_new_news + 1
            news['digest'] = news_digest

            if news['publishedAt'] is None:
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

            redis_client.set(news_digest, news)
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

            cloudAMQP_client.sendMessage(news)

    print "Fetched %d new news" % num_of_new_news

    cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)
