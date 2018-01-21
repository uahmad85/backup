#!/usr/bin/env python
import boto3
import sys
from tag_resources import ResTags

session = boto3.resource('ec2')
client_session = boto3.client('ec2')
resource_session = boto3.resource('ec2')


user_data_file = '/Users/sunahmad/bootstrap_staging.py'
fh = open(user_data_file)
instance_tag = Tags=[
    {
        'Key': 'Name',
        'Value': 'esdn'}]


#def mk_inst(session, dryrun=False,image_id='ami-21cd3a41', maxcount=1, sshkey='close5-lnp', subnet_id='subnet-43b5d227',
#            inst_type='t2.small'):
#    instance = session.create_instances( DryRun=dryrun, ImageId=image_id, MinCount=1, MaxCount=3, KeyName=sshkey,
#                                         SubnetId=subnet_id, InstanceType=inst_type, UserData=fh.read(),
#                                         SecurityGroups=['sg-8bbe33ed'],
#                                         IamInstanceProfile={'Name': 'read_only_access_for_ec2'})
#    return instance
#
# backend01 = 'subnet-43b5d227'
def create_instance(subnet_id, inst_type, resource_session=resource_session, dryrun=False,
                    image_id='ami-9abea4fb', maxcount=3, sshkey='close5-lnp', instance_sg='sg-8bbe33ed', public_ip=False):
    instance = resource_session.create_instances(DryRun=dryrun, ImageId=image_id, MinCount=1, UserData=fh.read(),
                                                 IamInstanceProfile={'Name': 'read_only_access_for_ec2'},
                                                 MaxCount=maxcount, KeyName=sshkey, InstanceType=inst_type,
                                                 NetworkInterfaces=[{'DeviceIndex': 0, 'SubnetId': subnet_id,
                                                                     'Groups': [instance_sg],
                                                                     'AssociatePublicIpAddress': public_ip}])
    return instance

instance = create_instance(subnet_id='subnet-3bca0a63', inst_type='t2.small',
                           image_id='ami-21cd3a41', public_ip=False)

instance_id = instance[0].id
tag_inst = ResTags(resource_session).tag_instance(False, instance_id, instance_tag)
print tag_inst