import yaml
from pymongo import MongoClient

with open('../config.yaml', 'r') as configFile:
    cfg = yaml.load(configFile)

MONGO_DB_HOST = cfg['mongodb']['host']
MONGO_DB_PORT = cfg['mongodb']['port']
DB_NAME = cfg['mongodb']['db_name']

client = MongoClient("%s:%d" % (MONGO_DB_HOST, MONGO_DB_PORT))

def get_db(db=DB_NAME):
	db = client[db]
	return db
