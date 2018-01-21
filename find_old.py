#!/usr/bin/python
import os 
import time
lst = []
for files in os.listdir('.'):
    if (time.time() - os.stat(files).st_mtime) > 604800:
        lst.append(files)
        print lst

for x in os.listdir('.'):
    if x not in lst:
        print x
      
