#send http requests to aimed server
import requests
import yaml

from json import loads

with open('../config.yaml', 'r') as configFile:
    cfg = yaml.load(configFile)

NEWS_API_ENDPOINT = cfg['news_api']['news_api_endpoint']
NEWS_API_KEY = cfg['news_api']['news_api_key']
ARTICLES_API = cfg['news_api']['articles_api']

CNN = 'cnn'
DEFAULT_SOURCES = [CNN]

Sort_By_Top = 'top'

#build an url to send http request
def buildUrl(end_point=NEWS_API_ENDPOINT, api_name=ARTICLES_API):
    return end_point + api_name

def getNewsFromSource(sources=DEFAULT_SOURCES, sortBy=Sort_By_Top):
    articles = []
    for source in sources:
        #content of the request, in each source we have to call api once
        payload = { 'apiKey' : NEWS_API_KEY,
                    'source' : source,
                    'sortBy' : sortBy }
        response = requests.get(buildUrl(), params=payload)
        res_json = loads(response.content)

        #Extract info from response
        if (res_json is not None and
            res_json['status'] == 'ok' and
            res_json['articles'] is not None):
            # populate news and add source into news.
            for news in res_json['articles']:
                news['source'] = res_json['source']
            # extend() to combine two list
            articles.extend(res_json['articles'])
    return articles
