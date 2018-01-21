#!/usr/bin/python
import re
file = raw_input('filename: ')
if len(file) == 0 : file = 'db_servers'
fh = open(file)
fhw = open('db_servers_hyp', 'w')

for host in (fh):
    host = host.split()
    correct_hyp = re.findall('\S.+db\d+.*', host[1])
    if len(correct_hyp) == 0 : continue
    print str(correct_hyp)[2:-2], str(host[0])[2:-2]
    #print str(host[0])[2:-2], host[1]
