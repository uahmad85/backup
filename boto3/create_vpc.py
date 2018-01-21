#!/usr/bin/env python
import boto3
import sys
from tag_resources import ResTags
from time import sleep

user_home = os.environ.get('HOME')
aws_config_file = user_home + '/.aws/config'

resource_session = boto3.resource('ec2')
client_session = boto3.client('ec2')
aws_stack_info = {}

# getting information about all the Vpcs in the region.
all_vpcs = client_session.describe_vpcs()

vlans = ['10.0.1.0/24', '10.0.2.0/24', '10.0.3.0/24', '10.0.4.0/24']

vpc_tag = Tags=[
    {
        'Key': 'Name',
        'Value': 'close5-dev-newer'},]


pub_tag = Tags=[
    {
        'Key': 'Name',
        'Value': 'public'},]

pri_tag = Tags=[
    {
        'Key': 'Name',
        'Value': 'private'},]

def mk_vpc(resource_session, dryrun=True):
    try:
        vpc = resource_session.create_vpc(DryRun=dryrun,
                                          CidrBlock='10.0.0.0/16',
                                          InstanceTenancy='default')
        return vpc
    except:
        err = sys.exc_info()
        print "Err: " + str(err[1])

raw_vpc_input = mk_vpc(resource_session, dryrun=False)

sleep(3)


waiter = client_session.get_waiter('vpc_available')
waiter.wait(DryRun=False, VpcIds=[vpc_id])

raw_vpc_tag = ResTags(resource_session).tag_vpc(False, vpc_id, vpc_tag)
print raw_vpc_tag

def parse_pvc_tag(raw_vpc_tag):
    tag = str(raw_vpc_tag).split()[2].split('=')[1].strip(')')[1:-4]
    return tag

vpc_tag = parse_pvc_tag(raw_vpc_tag)

#print vpc_tag
print vpc_tag



# collecting env info.
aws_stack_info['Vpc'] = {}
aws_stack_info['Vpc']['Id'] = vpc_id
aws_stack_info['Vpc']['Tag'] = vpc_tag


def get_availability_zones(client_session):
    az_list = []
    zones = client_session.describe_availability_zones()
    for zone in zones['AvailabilityZones']:
        az_list.append(zone['ZoneName'])
    return az_list


def mk_subnet(resource_session, vpcid, dryrun=True, cidrblk='10.0.1.0/24', az='us-west-2a'):
    try:
        subnet = resource_session.create_subnet(DryRun=dryrun, VpcId=vpcid,
                                                CidrBlock=cidrblk, AvailabilityZone=az)
        return subnet
    except:
        err = sys.exc_info()
        print "Err: " + str(err[1])

avail_zones = get_availability_zones(client_session)


def get_all_sub(subnets):
    subnet_list = []
    for sub in subnets:
        subnet = str(sub).split('=')[1].strip(')')[1:-1]
        subnet_list.append(subnet)
    return subnet_list

for index in range(len(avail_zones)):
    subnets = mk_subnet(resource_session, vpc_id, False, vlans[index], az=avail_zones[index])

subnet_ids= get_all_sub(subnets)

aws_stack_info['Vpc']['Subnets'] = subnet_ids
print aws_stack_info

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