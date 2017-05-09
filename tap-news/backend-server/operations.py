import json
import os
import sys
import pickle
import random
import redis
import yaml

from bson.json_util import dumps
from datetime import datetime

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_recommendation_service_client

from cloudAMQP_client import CloudAMQPClient

with open('../config.yaml', 'r') as configFile:
    cfg = yaml.load(configFile)

REDIS_HOST = cfg['redis']['host']
REDIS_PORT = cfg['redis']['port']
LOG_CLICKS_TASK_QUEUE_URL = cfg['cloudAMQP']['log_clicks_task_queue_url']
LOG_CLICKS_TASK_QUEUE_NAME = cfg['cloudAMQP']['log_clicks_task_queue_name']
NEWS_TABLE_NAME = cfg['mongodb']['news_table_name']
CLICK_LOGS_TABLE_NAME = cfg['mongodb']['click_logs_table_name']

NEWS_LIMIT = 100
NEWS_LIST_BATCH_SIZE = 10
USER_NEWS_TIME_OUT_IN_SECONDS = 60

# db=0 means using the first database of the 16 databases provided by redis
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)
cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    #the final list to be returened to the user
    sliced_news = []

    if redis_client.get(user_id) is not None:
        news_digest = pickle.loads(redis_client.get(user_id))

        # If begin_index is out of range, this will return empty list;
        # If end_index is out of range (begin_index is within the range), this
        # will return all remaining news ids.
        sliced_news_digest = news_digest[begin_index:end_index]
        print sliced_news_digest
        db = mongodb_client.get_db()
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest':{'$in':sliced_news_digest}}))
    else:
        db = mongodb_client.get_db()
        # Get 100 latest news from the database according to the publishedAt attribute
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        # In order to save memeory, we only store the digest of each news from total_news
        total_news_digest = map(lambda x:x['digest'], total_news)

        redis_client.set(user_id, pickle.dumps(total_news_digest))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)

        sliced_news = total_news[begin_index:end_index]

    # Get preference for the user
    preference = news_recommendation_service_client.getPreferenceForUser(user_id)
    topPreference = None

    if preference is not None and len(preference) > 0:
        topPreference = preference[0]

    for news in sliced_news:
        # Remove text field to save bandwidth
        del news['text']
        if news['class'] == topPreference:
            news['reason'] = 'Recommend'
        if news['publishedAt'].date == datetime.today().date():
            news['time'] = 'today'
    return json.loads(dumps(sliced_news))

def logNewsClickForUser(user_id, news_id):
    print "user click_logs collector!"
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': datetime.utcnow()}

    db = mongodb_client.get_db()
    db[CLICK_LOGS_TABLE_NAME].insert(message)

    # Send log task to machine learning service for prediction
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': str(datetime.utcnow())}
    cloudAMQP_client.sendMessage(message);
