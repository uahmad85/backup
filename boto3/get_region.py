#!/usr/bin/env python
import os
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
user_home = os.environ.get('HOME')
aws_config_file = user_home + '/.aws/config'

def get_region(aws_config_file):
    region = {}
    parser.read(aws_config_file)
    for sec in parser.sections():
        for key, val in parser.items(sec):
            region[key] = val
        return region

region = get_region(aws_config_file)
if region['region'] == 'us-west-1':
    print 'yes it is'
else:
    print 'no its not'