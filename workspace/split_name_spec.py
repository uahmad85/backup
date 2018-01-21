#!/usr/bin/python

file = raw_input('file name: ')
fh = open(file)
wf = 'hostnames'
w1f = 'specs'
wh = open(wf, 'w')
w1h = open(w1f, 'w')
for host in fh:
    host = host.split()
    #hname = (host[0] + '\n')
    #sp = (host[1] + '\n')
    wh.write(host[0] + '\n')
    w1h.write(host[1] + '\n')
wh.close()
w1h.close()
