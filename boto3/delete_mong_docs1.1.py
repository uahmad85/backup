#!/usr/bin/python
from pymongo import MongoClient, MongoReplicaSetClient
import logging
import os
import argparse
import sys
from time import sleep

parser = argparse.ArgumentParser(description='Usage: delete_mongo_docs.py -l limit')
parser.add_argument('-s', '--skip', action='store', type=int, help='skip number of users')
parser.add_argument('-l', '--limit', action='store', type=int, help='limit number of users to process at Once')
parser.add_argument('-r', '--range', action='store', type=int, help='limit number of times this sctip should run time * limit')
parser.add_argument('-q', '--query', action='store', default=False, help='query for anything in particular')
results = parser.parse_args()

limit = 0

#settings logging to keep track of all the deleted documents
log_file_path = os.getenv('HOME')
log_file = log_file_path  + '/' + 'deleted_docs.log'
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='[%(asctime)s %(levelname)s] (%(threadName)-10s) %(message)s')

if results.limit:
    limit = results.limit

if results.range:
    rang = results.range

#connecting to mongo
client = MongoClient('localhost', 27017)
db = client['close5-live']

#total_count = db.badges.find({"removed": True}).count()
total_count = db.badges.find({"resolvedAt": { "$exists": True } }).count()
all_docs = db.badges.find({"resolvedAt": { "$exists": True } }).limit(limit)
logging.info("Total number of documents that matchs the Query: %s" % total_count)

counter = 10000
for i in range(rang):
    for doc in all_docs:
        db.badges.remove(doc['_id'])
        counter -= 1
        if counter == 0:
            break
#    sleep(20)

#after_count = db.badges.find().count()
after_count = db.badges.find({"resolvedAt": { "$exists": True } }).count()
logging.info("Total deleted documents: %s -- current count: %s" % (limit, after_count))