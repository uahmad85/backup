#!/usr/bin/python

import re
import json
count = 0
data = {}
file = raw_input('file name: ' )
if len(file) == 0 : file = '/Users/sunahmad/Downloads/5da4c420346336ecc071284e88e1f6b3ce3bf48d.csv'

fh = open(file)
d = {}
for line in fh:
    line = line.strip(',')
    ip_host = re.findall('^\S+\.\S.*?', line)
    ip_or_host = str(ip_host)[2:-2]
    list_date = re.findall('\[\d+/\S+/\d.*]', line)
    date = str(list_date)[3:-3]
    print ip_or_host, date
    try:
      d[ip_or_host]['count'] += 1
      d[ip_or_host]['last_date'] = date
    except KeyError:
      d[ip_or_host] = {}
      d[ip_or_host]['count'] = 1
      d[ip_or_host]['last_date'] = date
    
      print d[ip_or_host]
    #print ip_or_host, date
    #print 'host or ipaddress: %s, date: %s' % (sip_host, sdate)
for k,v in d.iteritems():
    print "{} - {} - {}".format(k,v['count'], v['last_date'])
#print json.dumps(d, indent=2),
