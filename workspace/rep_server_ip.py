#!/usr/bin/env python
import re
import socket
next_server = None
rep_server = None
rep_server_ip = 0
server_name = socket.getfqdn()
num = int(server_name[5:7])
domain = ('.').join(server_name.split('.')[1:])
if num == 01:
    next_server = 'sqdtb02p1',domain
elif num == 2:
    next_server = 'sqdtb01p1',domain
elif num == 3:
    next_server = 'sqdtb04p1',domain
elif num == 4:
    next_server = 'sqdtb03p1',domain
elif num == 5:
    next_server = 'sqdtb06p1',domain
elif num == 6:
    next_server = 'sqdtb05p1',domain
elif num == 7:
    next_server = 'sqdtb08p1',domain
elif num == 8:
    next_server = 'sqdtb07p1',domain
elif num == 9:
    next_server = 'sqdtb10p1',domain
elif num == 10:
    next_server = 'sqdtb09p1',domain

rep_server = ('.').join(next_server)
rep_server_ip = socket.gethostbyname(rep_server)
print "%s=%s"%('rep_server_ip',rep_server_ip)
