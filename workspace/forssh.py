#!/usr/bin/python

import re
lst = []
count = 0
file = raw_input('file_name: ')
if len(file) == 0 : file = 'servers'
fh = open(file)

for server in fh:
    server = server.strip()
    ip = re.findall('^\d+\.\d+\.\d+\.\d+$', server)
    if len(ip) == 0 : continue
    count = count + 1
    lst.append(ip)
print lst, count 
