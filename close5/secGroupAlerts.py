#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import argparse

import boto3
from botocore.exceptions import ClientError


security_groups = list()
region_name = 'us-west-2'
profile_name='default'
userId = '712818841314'
topicArn = 'arn:aws:sns:us-west-2:712818841314:SecurityHole'
email_list = {}
counter = 0

parser = argparse.ArgumentParser(description='Usage: %s -r <region> -p <aws-profile> -t <sns-topicArn>' % __file__)
parser.add_argument('-p', '--profile_name', action='store', default=False, help='aws credentials for account to target.')
parser.add_argument('-t', '--topicarn', action='store', default=False, help='SNS topic Arn for sending alerts.')
parser.add_argument('-r', '--region', action='store', help='region to setup Env in. '
                                                           'Default region is set in your ~/HOME/.aws/config')
results = parser.parse_args()

if results.region:
  region_name = results.region

if results.profile_name:
  profile_name = results.profile_name

if results.topicarn:
  topicArn = results.topicarn

session = boto3.Session(region_name=region_name, profile_name=profile_name)
ec2 = session.client('ec2')
sns = session.client('sns')
resource = session.resource('ec2')
response = ec2.describe_security_groups()


def create_ingress_rules(resource, ipprotocol='tcp', sgid=None, useridgp=[], from_port=22, to_port=22):
  sg = resource.SecurityGroup(sgid)
  reponse = sg.authorize_ingress(IpPermissions=[
    {'IpProtocol': ipprotocol,
     'FromPort': from_port,
     'ToPort': to_port,
     'IpRanges': [
       {'CidrIp': '216.113.160.71/32'}, {'CidrIp': '216.113.160.72/32'},
       {'CidrIp': '172.31.0.0/16'}, {'CidrIp': '10.0.0.0/24'}],
     'UserIdGroupPairs': useridgp}
  ])
  return reponse


def revoke_ingress(resource, sgid=None, ipp='tcp', fp=22, tp=22):
  sg = resource.SecurityGroup(sgid)
  response = sg.revoke_ingress(IpProtocol=ipp, CidrIp="0.0.0.0/0", FromPort=fp, ToPort=tp)
  return response


for sgs in response['SecurityGroups']:
  sg = resource.SecurityGroup(sgs['GroupId'])
  if sg.ip_permissions:
    for x in range(len(sg.ip_permissions)):
      if 'FromPort' in sg.ip_permissions[x].keys():
        if 'IpRanges' in sg.ip_permissions[x].keys():
          for i in sg.ip_permissions[x]['IpRanges']:
            if sg.ip_permissions[x]['FromPort'] not in [80, 443, 8080, 123] and i['CidrIp'] == '0.0.0.0/0':
              sg.ip_permissions[0]['Tags'] = sg.tags
              email_list[counter] = sg.ip_permissions
              counter += 1
if email_list:
  jobj = json.dumps(email_list, indent=2)
  message = {"default": jobj}
  response = sns.publish(
    TargetArn=topicArn,
    Message=json.dumps(message),
    MessageStructure='json'
  )
