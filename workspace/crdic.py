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
                                                        'passwd=',
                                                        'host=',
                                                        'port=',
                                                        'unix_socket='])
ab = dict(options)
print ab
for opt, arg in options:
    if opt in ('-u', '--user'):
        user = arg
    elif opt in ('-p', '--password'):
        passwd = arg
    elif opt in ('-s', '--server'):
        server = arg
    elif opt in ('-P', '--port'):
        port = arg
    elif opt in ('-S','--socket'):
        unix_socket = arg
#iport = int(port)
credentials = {'user': user, 'passwd': password, 'host': server, 'unix_socket': unix_socket}
print credentials
