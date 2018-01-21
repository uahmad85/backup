#!/usr/bin/python
from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
import os, paramiko
optuser = None
parser.read('/Users/sunahmad/old_data/python/paramiko/.credentials')
cred = dict()
keypath = os.path.expanduser('~/.ssh/close5.pem')
pkey = paramiko.RSAKey.from_private_key_file(keypath)

for section in parser.sections():
    for key, val in parser.items(section):
        if optuser:
            cred['username'] = optuser
            cred['pkey'] = pkey
        else:
            cred['username'] = 'ubuntu'
            cred['pkey'] = pkey
    print cred