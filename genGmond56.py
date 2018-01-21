#!/usr/bin/env python

import threadpool
import socket
import os
import shutil

def doWork(srcFullPath):
    fqdn = os.path.splitext(os.path.basename(srcFullPath))[0]
    try:
        socket.gethostbyname(fqdn)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((fqdn, 22))
        shutil.move(srcFullPath, DEST_DIR)
    except Exception, e:
        pass
    return True
def print_result(request, result):
    pass
def handle_exception(request, exc_info):
    pass

BASE_DIR = '/tmp/gmond'
DEST_DIR = '/etc/ganglia/gmond.d/'
reqs = []
for clusterName in os.listdir(BASE_DIR):
    for hostConfFile in os.listdir(os.path.join(BASE_DIR, clusterName)):
        srcFullPath = os.path.join(BASE_DIR, clusterName, hostConfFile)
        reqs.append(srcFullPath)

pool = threadpool.ThreadPool(50)
requests = threadpool.makeRequests(doWork, reqs, print_result, handle_exception)
a = [pool.putRequest(req) for req in requests]
pool.wait()
