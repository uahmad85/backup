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
from elasticsearch.helpers import bulk
import elasticsearch
import threading
import logging
import argparse
import sys
import datetime

elas = Elasticsearch()
skip = 0
limit = 0

#command line arguments
parser = argparse.ArgumentParser(description='Usage: to index all the users or items ./index.py [ --user | --item ]')
parser.add_argument('-u', '--user', action='store', default=False, help='for users indexing')
parser.add_argument('-i', '--items', action='store', default=False, help='for items indexing')
parser.add_argument('-s', '--skip', action='store', type=int, help='skip number of users')
parser.add_argument('-l', '--limit', action='store', type=int, help='limit number of users to process at Once')
parser.add_argument('-r', '--range', action='store', type=int, help='limit number of times this sctip should run time * 50000 bulk index')
parser.add_argument('-q', '--query', action='store', default=False, help='query for anything in particular')
results = parser.parse_args()

#logging for the script
#logging.basicConfig(filename='/var/lib/elasticsearch/data/indexing/index_log.log', level=logging.DEBUG,
#                   format='[ %(asctime)s %(levelname)s] (%(threadName)-10s) %(message)s',)

#logging for Elasticsearch
tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.INFO)
#tracer.addHandler(logging.FileHandler('/var/lib/elasticsearch/data/indexing/es_trace.log'))
pp = pprint.PrettyPrinter(indent=4)

request_body = {
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}
user_map_body = {
    "user": {
        "properties": {
            "name.full": { "type": "string", "index": "not_analyzed" },
            "email": { "type": "string", "index": "not_analyzed" },
            "location": { "type": "geo_point" }
        }
    }
}
#
item_map_body = {
    "item": {
        "_parent": {
            "type": "user"
        },
        "properties": {
            "location": { "type": "geo_point" }
        }
    }
}

count = 0
file = '/data/indexing/counter'
fh = open(file, 'a')
fhr = open(file, 'r')
num = [i for i in fhr.read().split('\n') if i][-1]
int_num = int(num) or 1
INDEX_NAME = 'close5-dev'
bulk_data = []

#connection Mongo to replica
#client = MongoReplicaSetClient('localhost', 27017)
client = MongoClient('mongodb.dev.close5.com', 27017)
db = client['staging-close5']
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
limit = results.limit or 10000
query = results.query or {}
ran = results.range or 50
print "skip+ counter", skip
sleep(1)
#to keep track of iterations of the script.

if results.user:
    for n in range(ran):
        print "skip before query", skip
        print "limit after query", limit
        user_info = db.users.find().skip(skip).limit(limit)
        #    for x in user_info : print x
        skip = limit * (int_num + n)
        count = int_num + n
        fh.write(str(count) + '\n')
        print "skip after query", skip
        print "limit after query", limit
        sleep(1)
        #user_info = db.users.find().count()
        for user in user_info.batch_size(1024):
            data_dict = {}
            try:
                data_dict['location'] = ','.join([str(x).strip() for x in user['latestLoc']])
                data_dict['photos'] = [str(x).strip() for x in user['photos']]
                data_dict['watching'] = [str(x).strip() for x in user['watching']]
                data_dict['sold'] = [str(x).strip() for x in user['sold']]
                data_dict['unlisted'] = [str(x).strip() for x in user['unlisted']]
                data_dict['createdAt'] = user['createdAt'].isoformat()
                data_dict['facebookId'] = str(user['facebookId'].encode("utf8")).strip()
                data_dict['vanity'] = str(user['vanity'].encode("utf8")).strip()
                data_dict['selling'] = [str(x).encode("utf8").strip() for x in user['selling']]
                data_dict['email'] = str(user['email']).strip()
                data_dict['name']['first'] = str(user['name'].encode("utf8")).strip().lower()
                data_dict['name']['last'] = str(user['lastName'].encode("utf8")).strip().lower()
                data_dict['name']['full'] = "%s %s" % (str(user['name'].encode("utf8")).strip().lower(), str(user['lastName'].encode("utf8")).strip().lower())
                data_dict['pushToken'] = str(user['pushToken']).strip()
            except KeyError as err:
                print err
                data_dict['name'] = {}
                data_dict['name']['first'] = str(user['name'].encode("utf8")).strip().lower()
                data_dict['name']['last'] = str(user['lastName'].encode("utf8")).strip().lower()
                data_dict['name']['full'] = "%s %s" % (str(user['name'].encode("utf8")).strip().lower(), str(user['lastName'].encode("utf8")).strip().lower())
                data_dict['pushToken'] = str()
                data_dict['facebookId'] = str()
                data_dict['vanity'] = str()
                data_dict['selling'] = []
            op_dict = {
                "index": {
                    "_id": str(user['_id']).strip(),
                    "_index": INDEX_NAME,
                    "_type": 'user'
                }
            }
            bulk_data.append(op_dict)
            bulk_data.append(data_dict)
            # print bulk_data
        print INDEX_NAME
        #bulk index the data
        print("bulk indexing...")
        #res = elasticsearch.helpers.bulk(elas, bulk_data, doc_type="user", index="close5", chunk_size=1024, request_timeout=30)
        res = es.bulk(index = INDEX_NAME, body = bulk_data, timeout = 60, refresh = True)
        #print(" response: '%s'" % (res))
        print("results:")
        proc = Popen("%s %s %s" % ('curl', '-XGE', 'http://localhost:9200/close5-dev/user/_count?pretty'), shell=True).communicate()[0]
        proc
        sleep(1)
    fh.close()