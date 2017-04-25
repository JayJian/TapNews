import requests
import os
import random

from lxml import html

GET_CNN_NEWS_XPATH = '''//p[@class="zn-body__paragraph"]//text() | //div[@class="zn-body__paragraph"]//text()'''

#load user_agent.txt
USER_AGENT_FILE = os.path.join(os.path.dirname(__file__),'user_agents.txt')
USER_AGENTS = []

with open(USER_AGENT_FILE, 'r') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1])
random.shuffle(USER_AGENTS)

# get a random user-agent header from USER_AGENTS
def getHeaders():
    ua = random.choice(USER_AGENTS)
    headers = {
        "Connection":"close",
        "User-Agent": ua
    }
    return headers

def extract_news(news_rul):
    #Fetch html, use session_requests to cover yourself
    session_requests = requests.session()
    response = session_requests.get(news_rul, headers=getHeaders())

    news = {}

    try:
        #Parse html
        tree = html.fromstring(response.content)
        #Extract information
        news = tree.xpath(GET_CNN_NEWS_XPATH)
        # use '' to join the string elements of sequence
        news = ''.join(news)
    except Exception as e:
        print # coding=utf-8
        return {}

    return news