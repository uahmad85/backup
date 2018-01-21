#!/usr/bin/env python
import boto3
import sys
from tag_resources import ResTags
from time import sleep

session = boto3.resource('ec2')
client_session = boto3.client('ec2')
resource_session = boto3.resource('ec2')
config_client_session = boto3.client('autoscaling')


user_data_file = '/Users/sunahmad/bootstrap.py'
fh = open(user_data_file)
instance_tag = Tags=[
    {
        'Key': 'Name',
        'Value': 'core-api'}]


def create_launch_config(config_name, instancetype, image_id):
    launch_config = config_client_session.create_launch_configuration(
        LaunchConfigurationName=config_name,
        ImageId=image_id,
        KeyName='close5-lnp',
        SecurityGroups=['sg-d986d5be'],
        InstanceType=instancetype,
        UserData=fh.read(),
        IamInstanceProfile='read_only_access_for_ec2',
        AssociatePublicIpAddress=True)
    return launch_config
print create_launch_config('testrun', 't2.micro', 'ami-0bc0316b')

sleep(10)


def put_scaling_policy(name):
    response = config_client_session.put_scaling_policy(
        AutoScalingGroupName=name,
        PolicyName='scale_up',
        PolicyType='SimpleScaling',
        AdjustmentType='ChangeInCapacity',
        MinAdjustmentMagnitude=1,
        ScalingAdjustment=1,
        Cooldown=300,
        MetricAggregationType='Average')
    return response

#print put_scaling_policy('testrun')
