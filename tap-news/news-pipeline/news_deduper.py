# -*- coding: utf-8 -*-

import datetime
import os
import sys

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_topic_modeling_service_client
import msg_to_graphite
import system_log_client

from cloudAMQP_client import CloudAMQPClient
import yaml

with open('../config.yaml', 'r') as configFile:
    cfg = yaml.load(configFile)

DEDUPE_NEWS_TASK_QUEUE_URL = cfg['cloudAMQP']['dedupe_news_task_queue_url']
DEDUPE_NEWS_TASK_QUEUE_NAME = cfg['cloudAMQP']['dedupe_news_task_queue_name']

SLEEP_TIME_IN_SECONDS = 1

NEWS_TABLE_NAME = cfg['mongodb']['news_table_name']

SAME_NEWS_SIMILARITY_THRESHOLD = 0.9

cloudAMQP_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    print "handle_message from dedupe queue"
    if msg is None or not isinstance(msg, dict):
        system_log_client.logger.warn("Message is broken!")
        # print "Message is broken!"
        return
    #stop using str to convert from unicode to encoded text/bytes
    task = msg
    text = str(task['text'].encode('utf-8'))

    if text is None:
        return

    # get all recent news based on publishedAt
    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    db = mongodb_client.get_db()
    recent_news_list = list(db[NEWS_TABLE_NAME].find({'publishedAt': {'$gte': published_at_day_begin, '$lt': published_at_day_end}}))

    if recent_news_list is not None and len(recent_news_list) > 0:
        documents = [str(news['text'].encode('utf-8')) for news in recent_news_list]
        documents.insert(0, text)

        # Calculate similarity matrix
        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T

        print pairwise_sim.A
        rows, _ = pairwise_sim.shape

        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                # Duplicated news. Ignore.
                # print "Duplicated news. Ignore."
                system_log_client.logger.warn("Duplicated news. Ignore.")
                return
    task['publishedAt'] = parser.parse(task['publishedAt'])

    # Classify news
    # title = task['title']
    # if title is None:
    topic = news_topic_modeling_service_client.classify(task['description'])
    task['class'] = topic

    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)

while True:
    if cloudAMQP_client is not None:
        msg = cloudAMQP_client.getMessage()
        if msg is not None:
            # parse and process the work
            try:
                handle_message(msg)
                args = ['tap-news.AMQP.dedupe','1']
                msg_to_graphite.main(args)
            except Exception as e:
                # print e
                system_log_client.logger.error(e)
                pass
        cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)
