#!/usr/bin/env python

import sys
import argparse
import json
import boto3
from botocore.exceptions import ClientError


security_groups = list()
region_name = 'us-west-2'
userId = '712818841314'
sgid = 'sg-73be3315'

parser = argparse.ArgumentParser(description='Usage: create_env.py -e <environment> -r <region>')
parser.add_argument('-n', '--number_of_instances', action='store', type=int, help='number of instances, prod use only.')
parser.add_argument('-r', '--region', action='store', help='region to setup Env in. '
                                                           'Default region is set in your ~/HOME/.aws/config')
parser.add_argument('-d', '--delete', action='store', help='delete instance')
results = parser.parse_args()

if results.region:
    region_name = results.region

session = boto3.Session(region_name=region_name)
ec2 = session.client('ec2')
resource = session.resource('ec2')
response = ec2.describe_security_groups()


def create_ingress_rules(resource, ipprotocol='tcp', sgid=sgid, useridgp=[], from_port=22, to_port=22,
                         ipranges=[{'CidrIp': '216.113.160.71/32'}, {'CidrIp': '216.113.160.72/32'}]):
    sg = resource.SecurityGroup(sgid)
    reponse = sg.authorize_ingress(IpPermissions=[
        {'IpProtocol': ipprotocol,
         'FromPort': from_port,
         'ToPort': to_port,
         'IpRanges': ipranges,
         'UserIdGroupPairs': useridgp
        }])
    return reponse

sg = resource.SecurityGroup('sg-e9662b90')
print json.dumps(sg.ip_permissions, indent=2)
#try:
#    create_ingress_rules(resource, useridgp=[{'GroupId': sgid, 'UserId': userId}])
#except ClientError as err:
#    print err
#
#
#def revoke_ingress(resource, id=sgid):
#    sg = resource.SecurityGroup(id)
#    sg.revoke_ingress(IpProtocol="tcp", CidrIp="0.0.0.0/0", FromPort=22, ToPort=22)
#
#
#try:
#   revoke_ingress(
#            resource,
#            id=sgid
#    )
#except:
#    err = sys.exc_info()
#    print "ERR MSG: " + str(err[1])
