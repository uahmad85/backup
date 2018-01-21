#!/usr/bin/env python

###cat /etc/ganglia/gmetad.header; for f in `ls -1`; do echo "data_source ${f} `ls -1 ${f}/ | tr "\n" " " `"; done
import os
import socket
from threading import Thread
import Queue
import sys

NUM_PARALLEL = 50

def doWork():
    while True:
        clusterName, hostName = q.get()
        try:
            socket.gethostbyname(hostName)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((hostName, 8649))
            hosts[clusterName].append(hostName)
        except:
            pass
        finally:
            q.task_done()

BASE_DIR = '/tmp/gmetad'
header = open('/etc/ganglia/gmetad.header', 'rb').read()
hosts = {}
clustersToFollow = []
if len(sys.argv) == 2:
    clustersToFollow = sys.argv[1].split(',')

q = Queue.Queue(NUM_PARALLEL*2)
for i in range(NUM_PARALLEL):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()


for clusterName in os.listdir(BASE_DIR):
    hosts[clusterName] = []
    if len(clustersToFollow) == 0 or clusterName in clustersToFollow:
        for hostName in os.listdir(os.path.join(BASE_DIR, clusterName)):
            q.put((clusterName,hostName))
q.join()

outfile = open('/etc/ganglia/gmetad.conf', 'w')
outfile.write(header)
for clusterName in hosts.keys():
    if len(hosts[clusterName]) > 0:
        outfile.write('data_source ' + clusterName)
        for host in hosts[clusterName][0:5]:
            outfile.write(' ' + host)
        outfile.write('\n')
