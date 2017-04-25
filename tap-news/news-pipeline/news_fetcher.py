# -*- coding: utf-8 -*-

import os
import sys

from newspaper import Article

# import common and scraper package in parent directiory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__),'scrapers'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://yrvoxnud:H9FPhFT-9uee6ZNfOJstEZFi98SCKLcI@donkey.rmq.cloudamqp.com/yrvoxnud"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://lpxgjkmt:xvCbuMX-h7G6BGehoF_A3WWaLslUNp8g@donkey.rmq.cloudamqp.com/lpxgjkmt"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    # check whether msg is none or it's a json format
    if msg is None or not isinstance(msg, dict):
        print "Message is broken"
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
            except Exception as e:
                print # coding=utf-8
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
