#!/usr/bin/env python

import boto3
import sys
from tag_resources import ResTags

client_session = boto3.client('ec2')
resource_session = boto3.resource('ec2')

# getting information about all the Vpcs in the region.
all_vpcs = client_session.describe_vpcs()

pub_tag = Tags=[
    {
        'Key': 'Name',
        'Value': 'public'},]

pri_tag = Tags=[
    {
        'Key': 'Name',
        'Value': 'private'},]

def get_vpc_id(all_vpcs, vpc_tag):
    for vps in all_vpcs['Vpcs']:
        for tag in vps['Tags']:
            if vpc_tag in tag.values():
                vpc_id = vps['VpcId']
                return vpc_id

vpc =  get_vpc_id(all_vpcs, 'close5-dev-newer')
vpc_id = resource_session.Vpc(vpc)


def get_all_sub(vpc_id):
    subnet_list = []
    for sub in subnets:
        subnet = str(sub).split('=')[1].strip(')')[1:-1]
        subnet_list.append(subnet)
    return subnet_list

subnet_ids= get_all_sub(vpc_id)

print subnet_ids


def apply_tag(start, stop, tag, sub_ids=subnet_ids, dryrun=True):
    for n in range(start, stop):
        try:
            sub_tag = ResTags(resource_session).tag_subnet(dryrun, subnet_ids[n], tag)
            print sub_tag
        except:
            err = sys.exc_info()
            print "Err: " + str(err[1])


print apply_tag(1, 2, pub_tag, dryrun=False)

if len(subnet_ids) == 3:
    stop = 3
else:
    stop = 4
print apply_tag(2, stop, pri_tag, dryrun=False)
