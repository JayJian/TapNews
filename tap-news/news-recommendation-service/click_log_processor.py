# -*- coding: utf-8 -*-

'''
Time decay model:
If selected:
p = (1-α)p + α
If not:
p = (1-α)p
Where p is the selection probability, and α is the degree of weight decrease.
The result of this is that the nth most recent selection will have a weight of
(1-α)^n. Using a coefficient value of 0.05 as an example, the 10th most recent
selection would only have half the weight of the most recent. Increasing epsilon
would bias towards more recent results more.
'''

import news_classes
import os
import sys

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import system_log_client
from cloudAMQP_client import CloudAMQPClient
import yaml

with open('../config.yaml', 'r') as configFile:
    cfg = yaml.load(configFile)

NUM_OF_CLASSES = 17
INITIAL_P = 1.0 / NUM_OF_CLASSES
ALPHA = 0.1

SLEEP_TIME_IN_SECONDS = 1

PREFERENCE_MODEL_TABLE_NAME = cfg['mongodb']['preference_model_table_name']
NEWS_TABLE_NAME = cfg['mongodb']['news_table_name']

LOG_CLICKS_TASK_QUEUE_URL = cfg['cloudAMQP']['log_clicks_task_queue_url']
LOG_CLICKS_TASK_QUEUE_NAME = cfg['cloudAMQP']['log_clicks_task_queue_name']

cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

def handleMsg(msg):
    if msg is None or not isinstance(msg, dict):
        return

    if ('userId' not in msg
        or 'newsId' not in msg
        or 'timestamp' not in msg):
        return

    userId = msg['userId']
    newsId = msg['newsId']

    # update user's news preference
    db = mongodb_client.get_db()
    model = db[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId':userId})

    # if model not exist, create a basic new model
    if model is None:
        print 'Creating preference model for new user: %s' % userId
        new_model = {'userId':userId}
        preference = {}
        for topic in news_classes.classes:
            preference[topic] = float(INITIAL_P)
        new_model['preference'] = preference
        model = new_model
        db[PREFERENCE_MODEL_TABLE_NAME].insert(model)

    system_log_client.logger.info('Updating preference model for new user: %s' % userId)
    # print 'Updating preference model for new user: %s' % userId

    # Update model using time decaying method
    news = db[NEWS_TABLE_NAME].find_one({'digest': newsId})
    if (news is None
        or 'class' not in news
        or news['class'] not in news_classes.classes):
        print news is None
        print 'class' not in news
        print news['class'] not in news_classes.classes
        print 'Skipping processing...'
        return

    click_class = news['class']

    # update the clicked topic
    old_p = model['preference'][click_class]
    print old_p
    model['preference'][click_class] = float((1 - ALPHA)*old_p + ALPHA)
    print model['preference'][click_class]

    # update the not clicked topic
    for topic, prob in model['preference'].iteritems():
        if not topic == click_class:
            model['preference'][topic] = float((1-ALPHA)*model['preference'][topic])

    db[PREFERENCE_MODEL_TABLE_NAME].replace_one({'userId': userId}, model, upsert=True)

def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.getMessage()
            if msg is not None:
                # Parse and process the task
                try:
                    handleMsg(msg)
                except Exception as e:
                    system_log_client.logger.error(e)
                    pass
            # Remove this if this becomes a bottleneck.
            cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ ==  "__main__":
    run()
