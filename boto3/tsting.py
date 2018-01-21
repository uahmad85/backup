#!/usr/bin/env python
import boto3
import sys
import os
from tag_resources import ResTags
from ConfigParser import SafeConfigParser

resource_session = boto3.resource('ec2')
client_session = boto3.client('ec2')
parser = SafeConfigParser()
user_home = os.environ.get('HOME')
config_file = user_home + '/.aws/config'

Cidrs_pub = { 'public': ['10.0.1.0/24', '10.0.2.0/24']}
Cidrs_pri = {'private': ['10.0.2.0/24','10.0.3.0/24']}

pub_tag = Tags=[
    {
        'Key': 'Name',
               'Value': 'public'},]

pri_tag = Tags=[
    {
        'Key': 'Name',
        'Value': 'public'},]


def get_region(aws_config_file):
    region = {}
    try:
        parser.read(aws_config_file)
    except:
        err = sys.exc_info()
        print "ERR MSG: " + str(err[1])
        print "There is no .aws/config file for. Can not find region information"

    for sec in parser.sections():
        for key, val in parser.items(sec):
            region[key] = val
            return region

print get_region(config_file)