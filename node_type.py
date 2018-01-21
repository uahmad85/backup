#!/usr/bin/env python
import re
import socket
node_type=re.compile('\d*').split(socket.getfqdn())[0]
print "%s=%s"%('node_type',node_type)
