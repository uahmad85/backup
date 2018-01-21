#!/usr/bin/env python

import os
import socket
import shutil
from threading import Thread
import Queue

NUM_PARALLEL = 50

def doWork():
    while True:
      fqdn, srcFullPath = q.get()
      try:
        socket.gethostbyname(fqdn)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((fqdn, 8649))
        filesToMove.append(srcFullPath)
      except:
        pass
      finally:
        q.task_done()

BASE_DIR = '/tmp/gmond'
DEST_DIR = '/etc/ganglia/gmond.d/'
filesToMove = []
q = Queue.Queue(NUM_PARALLEL*2)
for i in range(NUM_PARALLEL):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()

for clusterName in os.listdir(BASE_DIR):
  for hostConfFile in os.listdir(os.path.join(BASE_DIR, clusterName)):
    fqdn = os.path.splitext(os.path.basename(hostConfFile))[0]
    srcFullPath = os.path.join(BASE_DIR, clusterName, hostConfFile)
    q.put((fqdn, srcFullPath))
q.join()

for f in filesToMove:
  try:
    shutil.move(f, DEST_DIR)
  except:
    pass
