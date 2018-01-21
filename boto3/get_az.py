#!/usr/bin/env python

import boto3

client_session = boto3.client('ec2')


def get_availability_zones(session):
    az_list = []
    zones = session.describe_availability_zones()
    for zone in zones['AvailabilityZones']:
        az_list.append(zone['ZoneName'])
    return az_list

print get_availability_zones(client_session)