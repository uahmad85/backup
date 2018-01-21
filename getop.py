#!/usr/bin/python
import getopt
import sys
import _mysql

user = None
password = None
server = None
#port = None
unix_socket = None

options, remainder = getopt.getopt(sys.argv[1:], 'u:p:s:P:S:', ['user=',
                                                        'password=',
                                                        'server=',
                                                        'port=',
                                                        'socket='])
for opt, arg in options:
    if opt in ('-u', '--user'):
        user = arg
    elif opt in ('-p', '--password'):
        password = arg
    elif opt in ('-s', '--server'):
        server = arg
    elif opt in ('-P', '--port'):
        port = arg
    elif opt in ('-S','--socket'):
        unix_socket = arg
#iport = int(port)
credentials = {'user': user, 'passwd': password, 'host': server, 'unix_socket': unix_socket}

con = _mysql.connect(**credentials)
con.query('show databases')
result = con.store_result()
dbs = result.fetch_row(0)
#print dbs

avoid_db = (('information_schema',), ('performance_schema',))

for db in dbs:
   if db in avoid_db : continue
   print db
