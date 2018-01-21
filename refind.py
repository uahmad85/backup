#!/usr/bin/python

import re

file = 'host_names'
fh = open(file)
name = raw_input('type regex: ')
for host in fh:
     myhost = re.findall(name, host)
     if myhost != []:
         my_host = '%s' % (myhost)
         hostnames = my_host[2:-2]
         print hostnames

