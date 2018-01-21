#!/usr/bin/python
from suprocess Popen, PIPE
file = "/etc/hosts"
fh = open(file)
old_dns = 10.0.0.1
for line in fh:
    if old_dns in line:
         print "Popen(['service' 'network' 'restart'], stdout=PIPE, shell=True).communicate"

