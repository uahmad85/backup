#!/usr/bin/env python
import boto3
import sys
from tag_resources import ResTags
import os
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
user_home = os.environ.get('HOME')
aws_config_file = user_home + '/.aws/config'
aws_access_file = user_home + '/.aws/credentials'
boto3.set_stream_logger('botocore')

def get_region(aws_config_file):
    region = {}
    parser = SafeConfigParser()
    parser.read(aws_config_file)
    for sec in parser.sections():
        for key, val in parser.items(sec):
            region[key] = val
        return region

config_region = get_region(aws_config_file)
cur_region = config_region['region']
user_data_file = '/Users/sunahmad/bootstrap.py'
fh = open(user_data_file)


class AutoScalingGroup():
    default_security_group = ['sg-d986d5be']
    default_protocol = 'http'
    default_instance_type = 'm4.large'
    default_image_id = 'ami-c9887ba9'
    default_iam_profile = 'read_only_access_for_ec2'
    default_tags = None
    default_subnets = ['subnet-30f0f969', 'subnet-0e855f6a']
    default_lc_name = 'core-api'
    default_sec_key = 'close5-lnp'
    default_vpc_zone_identifier = 'subnet-30f0f969, subnet-0e855f6a'

    def __init__(self, session):
        self.session = boto3.Session(region_name=cur_region)

    def create_elb(self, subnets=default_subnets, elb_port=80, in_port=80, elb_name=default_tags):
        client = self.session.client('elb')
        response = client.create_load_balancer(
            LoadBalancerName=elb_name,
            Subnets=subnets,
            SecurityGroups=self.default_security_group,
            Tags=[{'Key': 'Name', 'Value': self.default_tags}],
            Listeners=[{'Protocol': self.default_protocol, 'LoadBalancerPort': elb_port,
                        'InstanceProtocol': self.default_protocol, 'InstancePort': in_port,
                        'SSLCertificateId': 'close5.com'}])
        return response

    def create_launch_config(self, key_name=default_sec_key, security_group=default_security_group,
                             image_id=default_image_id, lc_name=default_lc_name, instance_type=default_instance_type):
        client = self.session.client('autoscaling')
        launch_config = client.create_launch_configuration(
            LaunchConfigurationName=lc_name,
            ImageId=image_id,
            KeyName=key_name,
            SecurityGroups=security_group,
            InstanceType=instance_type,
            UserData=fh.read(),
            IamInstanceProfile=self.default_iam_profile,
            AssociatePublicIpAddress=False)
        return launch_config

    def create_auto_scaling(self, min=2, max=10, as_name=default_tags,
                            lc_name=default_lc_name, vpcz_id=default_vpc_zone_identifier):
        client = self.session.client('autoscaling')
        response = client.create_auto_scaling_group(
            AutoScalingGroupName=as_name,
            LaunchConfigurationName=lc_name,
            MinSize=min, MaxSize=max,
            DesiredCapacity=min,
            HealthCheckGracePeriod=30,
            VPCZoneIdentifier=vpcz_id,
            LoadBalancerNames=[self.default_tags],
            HealthCheckType='ELB',
            DefaultCooldown=10,
            Tags=[{'Key': 'Name', 'Value': self.default_tags, 'PropagateAtLaunch': True}]
        )
        return response

    def put_scaling_policy(self, scaling_adjustment=None, policy_name="scaling up"):
        client = self.session.client('autoscaling')
        response = client.put_scaling_policy(
            AutoScalingGroupName=self.default_tags,
            PolicyName=policy_name,
            PolicyType='SimpleScaling',
            AdjustmentType='ChangeInCapacity',
            ScalingAdjustment=scaling_adjustment,
            Cooldown=300)
        return response

    def put_metric_alarm(self, as_name=default_tags, alarm_name=None, alarm_description= "scaling up policy", alarm_actions=None,
                         metric_name='CPUUtilization', comparison_operator='GreaterThanOrEqualToThreshold',
                         threshold=70):
        client = self.session.client('cloudwatch')
        response = client.put_metric_alarm(
            AlarmName=alarm_name,
            AlarmDescription=alarm_description,
            ActionsEnabled=True,
            AlarmActions=alarm_actions,
            Namespace='AWS/EC2',
            Statistic='Average',
            Dimensions=[
                {'Name': 'AutoScalingGroupName', 'Value': as_name}],
            MetricName=metric_name,
            ComparisonOperator=comparison_operator,
            Threshold=threshold,
            Unit='Seconds',
            Period=180,
            EvaluationPeriods=2)
        return response

