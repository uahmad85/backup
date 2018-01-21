#!/usr/bin/env python

import re

import boto3

session = boto3.Session(region_name='us-west-1', profile_name='prod')
eb_client = session.client('elasticbeanstalk')

apps = eb_client.describe_environments()

for x in apps['Environments']:
    app_name = re.findall(r'\w+-uat', x['EnvironmentName'])
    if not app_name == []:
        print app_name
