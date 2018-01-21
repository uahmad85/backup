#!/usr/bin/env python
import boto3


resource_session = boto3.resource('ec2')
client_session = boto3.client('ec2')

vlans = ['10.0.1.0/24', '10.0.2.0/24', '10.0.3.0/24', '10.0.4.0/24']


def get_availability_zones(client_session):
    az_list = []
    zones = client_session.describe_availability_zones()
    for zone in zones['AvailabilityZones']:
        az_list.append(zone['ZoneName'])
    return az_list


def mk_subnet(resource_session, vpcid, dryrun=True, cidrblk='10.0.1.0/24', az='us-west-2a'):
        subnet = resource_session.create_subnet(DryRun=dryrun, VpcId=vpcid,
                                                CidrBlock=cidrblk, AvailabilityZone=az)
        return subnet

avail_zones = get_availability_zones(client_session)

for index in range(len(avail_zones)):
    mk_subnet(resource_session, 'vpc-a2648dc6', True, vlans[index], az=avail_zones[index])
