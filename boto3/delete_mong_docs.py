#!/usr/bin/python
from pymongo import MongoClient, MongoReplicaSetClient
import logging
import os
import argparse

parser = argparse.ArgumentParser(description='Usage: delete_mongo_docs.py -l limit')
parser.add_argument('-s', '--skip', action='store', type=int, help='skip number of users')
parser.add_argument('-l', '--limit', action='store', type=int, help='limit number of users to process at Once')
parser.add_argument('-r', '--range', action='store', type=int, help='limit number of times this sctip should run time * 50000 bulk index')
parser.add_argument('-q', '--query', action='store', default=False, help='query for anything in particular')
results = parser.parse_args()

#settings logging to keep track of all the deleted documents
log_file_path = os.getcwd()
log_file = log_file_path  + '/' + 'deleted_docs.log'
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='[%(asctime)s %(levelname)s] (%(threadName)-10s) %(message)s')

if results.limit:
    limit = results.limit
#connecting to mongo
client = MongoClient('LOCALHOST', 27017)
db = client['close5-live']

total_count = db.badges.find().count()
all_docs = db.badges.find().limit(limit)
logging.info("Total number of documents that matchs the Query: %s" % total_count)
for doc in all_docs:
    db.badges.remove(doc['_id'])

after_count = db.badges.find().count()
remaining = total_count - after_count
logging.info("Total deleted documents: %s -- current count: %s" % (limit, after_count))