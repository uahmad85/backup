#!/usr/bin/env python

import boto3

client_session = boto3.client('ec2')
#correct_subnet = client_session.describe_subnets(DryRun=False, SubnetIds=['subnet-ce46b3aa',
#                                                                          'subnet-e1101996',
#                                                                          'subnet-2b121b5c',
#                                                                          'subnet-4474531d'], Filters=[{ "Name": "tag:Name",  "Values": [ "csa-public10.0.3.0/24-usw2b", ]}, ])
#print correct_subnet
#
#tag = "csa-public10.0.3.0/24-usw2b"
#print type(filter)
#
#
#0def sub_for_instance(client_session, sub_list, tag):
#    subnet = session.describe_subnets(DryRun=False, SubnetIds=sub_list, Filters=[ { "Name": "tag:Name",
#                                                                                    "Values": [ tag ] }, ])
#    for sub in subnet['Subnets']:
#        return sub['SubnetId']
#
#print sub_for_instance(client_session, ['subnet-ce46b3aa',
#                                  'subnet-e1101996',
#                                  'subnet-2b121b5c',
#                                  'subnet-4474531d'], tag)

def get_sub_id_from_tag(sub_tag, client_session=client_session):
    alls = client_session.describe_subnets()
    for sub in alls['Subnets']:
        if 'Tags' in sub.keys():
            if sub_tag in sub['Tags'][0].values():
                return sub['SubnetId']

sub_id = get_sub_id_from_tag('public02')
print sub_id
