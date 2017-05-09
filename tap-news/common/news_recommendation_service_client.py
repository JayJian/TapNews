import pyjsonrpc
import yaml

with open('../config.yaml', 'r') as configFile:
    cfg = yaml.load(configFile)

URL = cfg['services']['recommend_url']

client = pyjsonrpc.HttpClient(url=URL)

def getPreferenceForUser(userId):
    preference = client.call('getPreferenceForUser', userId)
    print "Preference list: %s" % str(preference)
    return preference
