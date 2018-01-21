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
user_data_file = '/Users/sunahmad/bootstrap.sh'
fh = open(user_data_file)


class CreateAutoScalingGroup():
    default_security_group = ['sg-d986d5be']
    default_protocol = 'http'
    default_instance_type = 't2.micro'
    default_image_id = 'ami-0bc0316b'
    iam_profile = 'read_only_access_for_ec2'

    def __init__(self, session):
        self.session = boto3.Session(region_name=cur_region)

    def create_elb(self, subnets, tags=None, elb_name='testrun', security_group=['sg-4c0aed2a']):
        client = self.session.client('elb')
        response = client.create_load_balancer(
            LoadBalancerName=elb_name,
            Subnets=subnets,
            SecurityGroups=security_group,
            Tags=[{'Key': 'Name', 'Value': tags}],
            Listeners=[{'Protocol': self.default_protocol, 'LoadBalancerPort': 80,
                        'InstanceProtocol': self.default_protocol, 'InstancePort': 9000,
                        'SSLCertificateId': 'arn:aws:iam::712818841314:server-certificate/close5.com'}])
        return response

    def create_launch_config(self, config_name='testrun', instance_type='t2.micro'):
        client = self.session.client('autoscaling')
        launch_config = client.create_launch_configuration(
            LaunchConfigurationName=config_name,
            ImageId=self.default_image_id,
            KeyName='close5-lnp',
            SecurityGroups=self.default_security_group,
            InstanceType=instance_type,
            UserData=fh.read(),
            IamInstanceProfile=self.iam_profile,
            AssociatePublicIpAddress=True)
        return launch_config

    def create_auto_scaling(self, as_name=None, config_name=None, elb_name='core-api', min=5, max=10):
        client = self.session.client('autoscaling')
        response = client.create_auto_scaling_group(
            AutoScalingGroupName=as_name,
            LaunchConfigurationName=config_name,
            MinSize=min, MaxSize=max,
            DesiredCapacity=min,
            HealthCheckGracePeriod=30,
            VPCZoneIdentifier='subnet-30f0f969, subnet-0d855f69',
            LoadBalancerNames=[elb_name],
            HealthCheckType='ELB',
            DefaultCooldown=10,
            Tags=[{'Key': 'Name', 'Value': 'consumer', 'PropagateAtLaunch': True}]
        )
        return response

    def put_scaling_policy(self, as_name=None, scaling_adjustment=None, pc_name="scaling up"):
        client = self.session.client('autoscaling')
        response = client.put_scaling_policy(
            AutoScalingGroupName=as_name,
            PolicyName=pc_name,
            PolicyType='SimpleScaling',
            AdjustmentType='ChangeInCapacity',
            ScalingAdjustment=scaling_adjustment,
            Cooldown=300)
        return response

    def put_metric_alarm(self, as_name=None, alarm_name=None, alarm_description= "scaling up policy", alarm_actions=None,
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

#print put_metric_alarm(alarm_name="scaling up", alarm_actions=[scaling_up_policy['PolicyARN']])
#print put_metric_alarm(alarm_name="scaling down", alarm_description='scaling down polity',
#                       alarm_actions=[scaling_down_policy['PolicyARN']],
#                       comparison_operator='LessThanOrEqualToThreshold', threshold=30)
