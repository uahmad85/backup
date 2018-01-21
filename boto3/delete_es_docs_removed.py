#!/usr/bin/env python

from subprocess import check_call
from time import sleep
import argparse
import logging
import sys
import json

try:
    from elasticsearch import Elasticsearch
except ImportError:
    check_call(["apt-get", "install", "-y", "python-pip"])
    check_call(["pip", "install", "elasticsearch"])
    from elasticsearch import Elasticsearch


# Command line arguments
parser = argparse.ArgumentParser(description='Usage: python delete_es_docs_removed.py -I <close5-dev> -s <500>')
parser.add_argument('-H', '--host', action='store', help='ES HOST NAME')
parser.add_argument('-I', '--index', action='store', help='index name')
parser.add_argument('-i', '--iterate', action='store', type=int, help='Number of iterations')
parser.add_argument('-s', '--size', action='store', type=int, help='total number of documents to delete per iteration')
results = parser.parse_args()

iterate = 1

# logging deleted documents
log_file = '/home/ubuntu/deleted_docs.log'
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='[%(asctime)s %(levelname)s] %(message)s')

# Elasticsearch settings
es_index = 'close5'
es_doc_type = 'item'
es_host = {
    "host": "localhost",
    "port": 9200
}

if results.index:
    es_index = results.index

if results.size:
    size = results.size

if results.iterate:
    iterate = results.iterate

if results.host:
    es_host = {"host": "%s" % results.host, "port": 9200}

query = '{"query": { "range": { "createdAt" : { "lte" : "now-180d/d" }}}}'
es = Elasticsearch(hosts=[es_host], timeout=3000)
del_docs = es.search(index=es_index, doc_type=es_doc_type, body=query, size=size)
for doc in del_docs['hits']['hits']:
    try:
        #print json.dumps(doc, indent=4)
        es.delete(index=es_index, doc_type=es_doc_type, id=doc['_id'])
    except:
        err = sys.exc_info()
        print str(err[0])
sleep(2)
tot_docs = es.search(index=es_index, doc_type=es_doc_type, body=query)
logging.info("Total number of remaining documents that matched the Query: %s" % tot_docs['hits']['total'])
