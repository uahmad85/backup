#!/usr/bin/python
## coding: utf-8
from time import asctime
from time import sleep
from subprocess import Popen, PIPE
import pprint
import pymongo
import json
from pymongo import MongoClient, MongoReplicaSetClient
from elasticsearch import Elasticsearch
import threading
import logging
import argparse
import sys

skip = 0
limit = 0

#command line arguments
parser = argparse.ArgumentParser(description='Usage: to index all the users or items ./index.py [ --user | --item ]')
parser.add_argument('-u', '--user', action='store', default=False, help='for users indexing')
parser.add_argument('-i', '--items', action='store', default=False, help='for items indexing')
parser.add_argument('-s', '--skip', action='store', type=int, help='skip number of users')
parser.add_argument('-l', '--limit', action='store', type=int, help='limit number of users to process at Once')
parser.add_argument('-r', '--range', action='store', type=int, help='limit number of time this sctip should time * 50000 bulk index')
parser.add_argument('-d', action='store', default=False, help='date in [YYYYYMMDD] format')
results = parser.parse_args()

#logging for the script
#logging.basicConfig(filename='/var/lib/elasticsearch/data/indexing/index_log.log', level=logging.DEBUG,
#                    format='[ %(asctime)s %(levelname)s] (%(threadName)-10s) %(message)s',)

#logging for Elasticsearch
tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.INFO)
#tracer.addHandler(logging.FileHandler('/var/lib/elasticsearch/data/indexing/es_trace.log'))
pp = pprint.PrettyPrinter(indent=4)

request_body = {
    "settings" : {
        "number_of_shards": 3,
        "number_of_replicas": 1
    }
}
count = 0
file = '/var/lib/elasticsearch/data/indexing/counter_item'
fh = open(file, 'a')
fhr = open(file, 'r')
num = [i for i in fhr.read().split('\n') if i][-1]
int_num = int(num) or 1
INDEX_NAME = 'close5'
bulk_data = []

#connection Mongo to replica
client = MongoReplicaSetClient('172.31.30.123', 27017)
db = client['close5-live']
colls = db.collection_names(include_system_collections=False)

# in case index (close5) does not exist.
ES_HOST = {
    "host" : "localhost",
    "port" : 9200
}

es = Elasticsearch(hosts = [ES_HOST], timeout = 3000)

if not es.indices.exists(INDEX_NAME):
    print("creating '%s' index..." % (INDEX_NAME))
    res = es.indices.create(index = INDEX_NAME, body = request_body)
    print(" response: '%s'" % (res))
    res_map = es.indices.put_mapping(index = INDEX_NAME, doc_type = 'user', body = user_map_body)
    print(" response: '%s'" % (res_map))
    res_item = es.indices.put_mapping(index = INDEX_NAME, doc_type = 'item', body = item_map_body)
    print(" response: '%s'" % (res_item))

inital_skip = results.skip or 0
print"inital_skip %s" % results.skip
skip = int_num * inital_skip or 1
print "counter + skip", skip
sleep(3)
limit = results.limit or 15000
query = ""
ran = results.range or 50
#to keep track of iterations of the script.
print 'all is fine til here'
if results.items:
    for n in range(ran):
        skip = limit * (int_num + n)
        print "skip:", skip
        print "limit:", limit
        sleep(2)
        count = int_num + n
        fh.write(str(count) + '\n')
        print skip
        user_info = db.items.find().skip(skip).limit(limit)
        #user_info = db.users.find().count()
        for user in user_info.batch_size(1024):
            data_dict = {}
            try:
                data_dict['location'] = ','.join([str(x).strip() for x in user['loc']])
                data_dict['category'] =  [str(x).strip() if len(user['category']) != 0 else ['empty'] for x in user['category'] ]
                data_dict['createdAt'] = str(user['createdAt']).strip()
                data_dict['updatedAt'] = str(user['updatedAt']).encode("utf8").strip()
                data_dict['soldAt'] = str(user['soldAt']).encode("utf8").strip()
                data_dict['live'] = str(user['live']).strip()
                data_dict['removed'] = str(user['removed']).strip()
                data_dict['status'] = str(user['status']).strip()
                data_dict['userId'] = str(user['userId']).strip()
                data_dict['buyerId'] = str(user['buyerId']).strip()
                data_dict['price'] = user['price']
                data_dict['featured'] = user['featured']
                data_dict['watchers'] = [str(x).strip() for x in user['watchers']]
                data_dict['answers'] = [str(x).strip() if len(user['answers']) != 0 else ['empty'] for x in user['answers'] ]
            except KeyError as err:
                print err
                data_dict['live'] = str(user['live']).strip()
                data_dict['removed'] = ""
                data_dict['status'] = str(user['status']).strip()
                data_dict['updatedAt'] = str(user['updatedAt']).encode("utf8").strip()
                data_dict['userId'] = str(user['_id']).strip()
                data_dict['price'] = user['price']
                data_dict['watchers'] = [str(x).strip() for x in user['watchers']]
                data_dict['answers'] = []

            op_dict = {
                "index": {
                    "_id": str(user['_id']).strip(),
                    "_index": INDEX_NAME,
                    "_type": 'item',
                    "_parent": str(user['userId']).strip(),
                }
            }
            bulk_data.append(op_dict)
            bulk_data.append(data_dict)
            # print bulk_data
        print INDEX_NAME
        #bulk index the data
        print("bulk indexing...")
        res = es.bulk(index = 'close5', body = bulk_data, timeout = 60, refresh = True)
        #print(" response: '%s'" % (res))
        print("results:")
        proc = Popen("%s %s %s" % ('curl', '-XGE', 'http://localhost:9200/close5/item/_count?pretty'), shell=True).communicate()[0]
        proc
        sleep(1)
    fh.close()
