#!/usr/bin/python

import re
file = raw_input('filename: ')
if len(file) == 0 : file = 'serhyp'
fh = open(file)
fhw = open('db_servers_hyp', 'w')

for host in (fh):
    host = host.split() 
    if len(host) != 0:
        db = host[0]
        if 'sqdtb' in db:
            print db, 'MySQL-5.6'
        if 'bidtb' == db:
            print 'MySQL-5.1'
         
        #print str(host[0].strip("'"))
