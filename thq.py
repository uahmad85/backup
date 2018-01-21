#!/usr/bin/python

import Queue
import threading
import logging
import time

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )
mq = Queue.Queue()

def myq(q):
    while not q.empty():
        x = q.get()
        print x
        q.task_done()

for i in range(10):
    mq.put(i)

#def mythread(th, q):
#    try:
#        t = threading.Thread(target=th, args=(q,))
#        t.setDaemon(True)
#        t.start()
#        logging.debug('starting %s', t.getName())
#    except Queue.Empty:
#        print 'empty que'
#        raise StopIteration

def run_parallel(as, q):
    if len(q.queue) != 0:
        num = q.get()
        t = threading.Thread(name=num, target=t, args=(q,))
        t.setDaemon(True)
        t.start()
        logging.debug('Starting thread %s', t.getName())

run_parallel(myq, mq)
main_t = threading.currentThread()
for t in threading.enumerate():
    if t is main_t:
        continue
    logging.debug('joining %s', t.getName())
    t.join()
