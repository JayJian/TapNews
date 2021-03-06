# -*- coding: utf-8 -*-

import os
import sys

from newspaper import Article

# import common and scraper package in parent directiory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__),'scrapers'))

import cnn_news_scraper
import msg_to_graphite
from cloudAMQP_client import CloudAMQPClient
import system_log_client
import yaml

with open('../config.yaml', 'r') as configFile:
    cfg = yaml.load(configFile)

DEDUPE_NEWS_TASK_QUEUE_URL = cfg['cloudAMQP']['dedupe_news_task_queue_url']
DEDUPE_NEWS_TASK_QUEUE_NAME = cfg['cloudAMQP']['dedupe_news_task_queue_name']
SCRAPE_NEWS_TASK_QUEUE_URL = cfg['cloudAMQP']['scrape_news_task_queue_url']
SCRAPE_NEWS_TASK_QUEUE_NAME = cfg['cloudAMQP']['scrape_news_task_queue_name']

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    # check whether msg is none or it's a json format
    if msg is None or not isinstance(msg, dict):
        # print "Message is broken"
        system_log_client.logger.warn("Message is broken!")
        return

    task = msg

    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text
    dedupe_news_queue_client.sendMessage(task)

while True:
    # fetch msg from queue
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            #handle the msg
            try:
                handle_message(msg)
                args = ['tap-news.AMQP.scrape','1']
                msg_to_graphite.main(args)
            except Exception as e:
                system_log_client.logger.error(e)
                # print e
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
