#!/usr/bin/python
import time
#from threading import thread
import threading 
exitFlag = 0
def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            thread.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1
print_time('new', 1, 3)
