#!/usr/bin/python
import sys, getopt
from Queue import Queue
from threading import Thread
import datetime
import boto3
import json
import os
import argparse
from pymongo import MongoClient


# Global variables
num_threads = 30

# ./m2s.py --host 172.31.30.123 -d close5-live -c items -f items2.json --day -2 -q testtesttest
# export to a json file with _id only will improve the stability
# mongoexport -h 172.31.30.123 -d close5-live -c items -o items.json -f "_id"
# db.items.find({ $and: [ {"updatedAt":{$gt: ISODate(new Date((new Date().getTime() - 1*86400*1000)).toISOString())}}, { removed: false } ] }).count()

parser = argparse.ArgumentParser(description='Create reindex tasks in sqs, Usage e.g. ./m2s.py --host 172.31.30.123 -d close5-live -c users -f users1.json -q mongo-qp-esreindex')
parser.add_argument('-d', '--db', action='store', default='staging-close5', help='mongodb database')
parser.add_argument('-c', '--collection', action='store', default='items', help='mongodb collection')
parser.add_argument('-p', '--port', action='store', type=int, default=27017, help='mongodb collection')
parser.add_argument('--host', action='store', default=False, help='mongodb hostname')
parser.add_argument('-k', '--slaveOk', action='store', default=False, help='allow secondary reads if available')
parser.add_argument('-q', '--queue', action='store', default='testtesttest', help='SQS queue name')
parser.add_argument('-f', '--file', action='store', default='', help='Import/cache data from the file, this will enable ---days switch to query updates in the past few days.')
parser.add_argument('--days', action='store', type=int, default=0, help='Negtive number e.g. -2, for the updated record in the past 2 Days')
parser.add_argument('--aws_access_key_id', action='store', default='AKIAJCUOPSCYFN3KVUAA', help='aws access key')
parser.add_argument('--aws_secret_access_key', action='store', default='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', help='aws secret key')
parser.add_argument('--region_name', action='store', default='us-west-1', help='aws region for sqs')

args = parser.parse_args()

exported_idfile = args.file
aws_sqs_queuename = args.queue
aws_access_key_id = args.aws_access_key_id
aws_secret_access_key = args.aws_secret_access_key
region_name = args.region_name
mongo_host = args.host
mongo_port = args.port
db_name = args.db
collection_name = args.collection
slaveOk = args.slaveOk
exported_idfile = args.file
days_offset=args.days




# Log start time for measurement
ts = datetime.datetime.now()
print ts


# Initializing some objects

id_queue = Queue()



# prepare sqs resource
sqsres = boto3.resource(
        'sqs',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
)




# worker function to task message array in the id_queue then batch send to AWS SQS
# msg format
#{"title":"Reindex item: 53fcc82a45b6f4db35000001","type":"item","id":"53fcc82a45b6f4db35000001"}
#{"title":"Reindex user: 54137ffc68d79e446c0001e2","type":"user","id":"54137ffc68d79e446c0001e2"}


def send2sqsworker(i,q):
    queue = sqsres.get_queue_by_name(QueueName=aws_sqs_queuename)

    while True:
        idList = q.get()
        entries = []
        for sid in idList:

            if collection_name == 'items':
                msgbody = '{"title":"Reindex item: ' + sid + '","type":"item","id":"' + sid + '"}'
            elif collection_name == 'users':
                msgbody = '{"title":"Reindex user: ' + sid + '","type":"user","id":"' + sid + '"}'
            else:
                print 'ERROR! no template found for collection name: ' + collection_name

            entries.append({'Id': sid, 'MessageBody': msgbody})
        response = queue.send_messages(Entries=entries)
        ok_items = response.get('Successful')
        if ok_items and len(ok_items) < 10:
            print 'Batch sent with success items < 10: ' + str(len(ok_items))
            print response
        # Print out any failures
        failed_items = response.get('Failed')
        if failed_items:
            print failed_items
        q.task_done()



# Create a number of worker threads
for i in range(num_threads):
    worker = Thread(target=send2sqsworker, args=(i, id_queue,))
    worker.setDaemon(True)
    worker.start()




# Main thread to populate id_queue with mongodb record _id and grouping the in arrays with 10 records

cnt = 0
idbuf = []
# mongoexport -h 172.31.30.123 -d close5-live -c items -o items.json -f "_id"

query = '{}'
if collection_name == 'items':
    if days_offset == 0:
        query = '{ "live": true }'
    else:
        start_date = (datetime.datetime.utcnow() + datetime.timedelta(days=days_offset)).isoformat() + 'Z'
        query = '{ $and: [ {"updatedAt":{$gt: ISODate("' + start_date + '")}}, {"live": true}  ] }'


if collection_name == 'users' and days_offset < 0:
    start_date = (datetime.datetime.utcnow() + datetime.timedelta(days=days_offset)).isoformat() + 'Z'
    query = '{"updatedAt":{$gt: ISODate("' + start_date + '")}}'


if len(exported_idfile) > 1 and not os.path.isfile(exported_idfile):
    print 'File: '+ exported_idfile + 'Not found, Start mongoexport command to get the records'
    queryesc = json.dumps(query)
    shell_cmd = 'mongoexport -h '+ mongo_host +' -d ' + db_name + ' -c '+ collection_name +' -o '+ exported_idfile + ' -q '+ queryesc +' -f "_id"'
    print shell_cmd
    os.system(shell_cmd.replace('$','\$'))


if len(exported_idfile) > 1:
    print 'File: '+ exported_idfile + ' found, getting oids from it'
    with open(exported_idfile, "r") as ins:
        # Create IDs in batch of 10
        for line in ins:
            d1 = json.loads(line)
            sid = str(d1['_id']['$oid'])
            idbuf.append(sid)
            cnt = cnt + 1
            if len(idbuf) > 9:
                id_queue.put(idbuf[:])
                del idbuf[:]
        # Leftover ids
        if len(idbuf) > 0:
            print 'Shipping of last: ' + str(len(idbuf))
            id_queue.put(idbuf[:])
            del idbuf[:]


else:
    mongo_url = 'mongodb://'+mongo_host+':'+str(mongo_port)
    if slaveOk:
        client = MongoClient(mongo_url,slaveOK=True)
    else:
        client = MongoClient(mongo_url)

    db = client[db_name]
    col = db[collection_name]
    # Python json load doesn't work for mongo query json format
    #json_query = json.loads(query)
    cur = col.find()


    # Create IDs in batch of 10
    for item in cur:
        sid = str(item['_id'])
        idbuf.append(sid)
        cnt = cnt +1
        if len(idbuf) > 9:
            id_queue.put(idbuf[:])
            del idbuf[:]
    # Leftover ids
    if len(idbuf) > 0:
        print 'Shipping of last: ' + str(len(idbuf))
        id_queue.put(idbuf[:])
        del idbuf[:]




print '------' + str(cnt) + '---Records in id_queue-----'
print '*** Main thread waiting'
id_queue.join()

tf = datetime.datetime.now()
te = tf - ts
print '*** Done with %d threads ****** time used: ' % num_threads
print te