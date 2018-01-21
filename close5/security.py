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


parser = argparse.ArgumentParser(description='Usage: %s -r <region>' % __file__)
parser.add_argument('-p', '--profile_name', action='store', type=int, help='aws credentials for account to target.')
parser.add_argument('-r', '--region', action='store', help='region to setup Env in. '
                                                           'Default region is set in your ~/HOME/.aws/config')
results = parser.parse_args()

if results.region:
    region_name = results.region

if results.profile_name:
    profile_name = results.profile_name

session = boto3.Session(region_name=region_name, profile_name=profile_name)
ec2 = session.client('ec2')
sns = session.client('sns')
resource = session.resource('ec2')
response = ec2.describe_security_groups()


def create_ingress_rules(resource, ipprotocol='tcp', sgid=None, useridgp=[], from_port=22, to_port=22,
                         ipranges=[{'CidrIp': '216.113.160.71/32'}, {'CidrIp': '216.113.160.72/32'}]):
    sg = resource.SecurityGroup(sgid)
    reponse = sg.authorize_ingress(IpPermissions=[
        { 'IpProtocol': ipprotocol,
          'FromPort': from_port,
          'ToPort': to_port,
          'IpRanges': ipranges,
          'UserIdGroupPairs': useridgp
          }])
    return reponse


def revoke_ingress(resource, id=None):
    sg = resource.SecurityGroup(id)
    response = sg.revoke_ingress(IpProtocol="tcp", CidrIp="0.0.0.0/0", FromPort=22, ToPort=22)
    return response


def key_exists(sg, key):
    for x in range(len(sg.ip_permissions)):
        if sg.ip_permissions[x][key]:
            return True
        else:
            continue


#def val_exists(sg, val):
#    for x in range(len(sg.ip_permissions))

for sgs in response['SecurityGroups']:
    sg = resource.SecurityGroup(sgs['GroupId'])
    if sg.ip_permissions:
        for x in range(len(sg.ip_permissions)):
            if 'FromPort' in sg.ip_permissions[x].keys():
                if sg.ip_permissions[x]['FromPort'] in [0, 22, 27017, 9200]:
                    if 'IpRanges' in sg.ip_permissions[x].keys():
                        if sg.ip_permissions[x]['IpRanges']:
                            for i in sg.ip_permissions[x]['IpRanges']:
                                if i['CidrIp'] == '0.0.0.0/0':
                                    sg.ip_permissions[0]['Tags'] = sg.tags
                                    print sg.ip_permissions[x]
                            #print sg.ip_permissions[x]['FromPort'], sg.ip_permissions[x]['IpRanges']

                    #    print sg.ip_permissions[x]['FromPort']
                        #for x in range(len(sg.ip_permissions))):
                        #for x in range(len(sg.ip_permissions)):
                        #    if sg.ip_permissions[x]['IpRanges']:
                        #        if any(sg.ip_permissions[0]['IpRanges'][x]['CidrIp'] == '0.0.0.0/0'
                        #               for x in range(len(sg.ip_permissions[0]['IpRanges']))):
                        #            sg.ip_permissions[0]['Tags'] = sg.tags
                        #            print json.dumps(sg.ip_permissions[0], indent=2)
                        #jobj = json.dumps(sg.ip_permissions[0], indent=2)
                        #message = {"default": jobj}
                        #response = sns.publish(
                        #        TargetArn='arn:aws:sns:us-west-2:712818841314:SecurityHole',
                        #        Message=json.dumps(message),
                        #        MessageStructure='json'
                        #)
                        #try:
                        #    revoke_ingress(resource, id=sg.id)
                        #except ClientError as err:
                        #    print err

                        #try:
                        #    create_ingress_rules(resource, sgid=sg.id,
                        #                         useridgp=[{'GroupId': sg.id, 'UserId': userId}])
                        #except ClientError as err:
                        #    print err
