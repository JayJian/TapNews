import pyjsonrpc
import system_log_client
import yaml

with open('../config.yaml', 'r') as configFile:
    cfg = yaml.load(configFile)

URL = cfg['services']['modeling_url']

client = pyjsonrpc.HttpClient(url=URL)

def classify(text):
    topic = client.call('classify', text)
    # print "Topic: %s" % str(topic)
    system_log_client.logger.info("Topic: %s" % str(topic))
    return topic
