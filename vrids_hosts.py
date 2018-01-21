#!/usr/bin/python
import sys
import re
import json
dic = dict()
lst = list()
vrlst = list()
xlst = list()
file = sys.argv[1]
try:
    fh = open(file)
except IOError as io:
    print io
    exit()

for host in fh:
    host = host.strip()
    hostname = re.findall('^devops@sqdtb\S+', host)
    vrid = re.findall('virtual.*', host)
    strhost = str(hostname)[2:-4]
    strvrid = str(vrid)[2:-2]
    if len(strhost) != 0 and len(strvrid) != 0:
        hostn = strhost.split('@')[1]
        lst.append(hostn)
vrlst.append(strvrid)
print [(x , y) for x in lst for y in vrlst]
