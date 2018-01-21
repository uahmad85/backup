#!/usr/bin/python
import re
file = '/Users/uahmad/web.log'
lst = list()
cont = 0
dic = dict()
lines = open(file)
for line in lines:
    host_ip = re.findall(r'(^\S+\.\S+\.\S+?) \- \- \[(\d{2}\/\w{3,4}\/\d{4}\:\w{2}\:\w{2}\:\w{2})' , line)
    if len(host_ip) != 0:
        hosts_date = host_ip[0]
        hosts, date = hosts_date
#        dic[hosts] = dic.get(hosts,0) + 1
        dic[hosts] = {}
        dic[hosts]['count'] = dic[hosts].get('count', 0) + 1
    else:
        dic[hosts]['count'] = dic[hosts].get('count', 1)
        print dic[hosts].get('count')
#        try:
#            dic[hosts]['count'] = dic[hosts]['count'] + 1
#            dic[hosts]['last_date'] = date
#        except KeyError as key:
#            dic[hosts] = {}
#            dic[hosts]['count'] = 1
#            dic[hosts]['last_date'] = date
#print dic
#for key, val in dic.items():
#    lst.append((val['count'], key) )
#    lst.sort(reverse=True)
#    
#for host in lst[:10]:
#    cont += 1
#    print "Top {0} Output: {1} - {2} - {3}".format(cont, host[1], host[0], dic[hosts]['last_date'])
