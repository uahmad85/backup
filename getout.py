#!/usr/bin/python

import re, sys
import Queue

que_host = Queue.Queue()

fle = '/Users/sunahmad/old_data/python/paramiko/host_names'
fh = open(fle)
regex = sys.argv[1]
optarg = 'host1,host2'

def host_list(reg, fh, hosts=optarg):
    if ',' in hosts:
        for host in hosts.split(','):
            que_host.put(host)
        return que_host
#    else:
#        if '*' in hosts:
#            for host in fh:
#                my_host = re.findall(reg, host)
#                if not my_host == []:
#                    hostname = '%s' % (my_host)
#                    que_host.put(hostname[2:-2])
#        return que_host

print host_list(regex, fh)