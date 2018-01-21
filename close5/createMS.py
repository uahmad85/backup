#!/usr/bin/env python

import boto3
import sys
import os
from ConfigParser import SafeConfigParser
import argparse

default_vpc = 'vpc-48739c2c'
userId = '712818841314'
default_image = 'ami-78aa7f18'
default_inst_type = 't1.micro'

parser = argparse.ArgumentParser(description='Usage: create_env.py -e <environment> -r <region>')
parser.add_argument('-i', '--image', action='store', help='Image Id to be use, default is ' + default_image)
parser.add_argument('-s', '--service_name', action='store', help='New Service Name')
parser.add_argument('-t', '--instance_type', action='store', help='Instance type to be used, default is ' + default_inst_type)
parser.add_argument('-e', '--environment', action='store', help='environment name')
parser.add_argument('-n', '--number_of_instances', action='store', type=int, help='number of instances, prod use only.')
parser.add_argument('-r', '--region', action='store', help='region to setup Env in. '
                                                           'Default region is set in your ~/HOME/.aws/config')
parser.add_argument('-d', '--delete', action='store', help='delete instance')
results = parser.parse_args()

parser = SafeConfigParser()
user_home = os.environ.get('HOME')
aws_config_file = user_home + '/.aws/config'
aws_access_file = user_home + '/.aws/credentials'

access_keys_and_region_not_found = "Please make sure that both files %s and %s exist " \
                                   "\nand have region, aws_access_key_id and aws_secret_access_key configured properly." \
                                   "\nIf both of these files exists and you still seeing this message." \
                                   "\nPlease contact with your administrator for proper privileges." \
                                   "\nif you have awscli installed, please execute 'aws configure' command and follow the instructions." \
                                   "\n[default] " \
                                   "\nregion=region_name" % (aws_access_file, aws_config_file)

if not os.path.isfile(aws_access_file):
    print "Access Keys not founnd. " + access_keys_and_region_not_found
    sys.exit()

if not os.path.isfile(aws_config_file):
    print "Region not founnd " + access_keys_and_region_not_found
    sys.exit()


def get_region(aws_config_file):
    region = {}
    parser = SafeConfigParser()
    parser.read(aws_config_file)
    for sec in parser.sections():
        for key, val in parser.items(sec):
            region[key] = val
        return region

if results.region:
    cur_region = results.region
else:
    config_region = get_region(aws_config_file)
    cur_region = config_region['region']

session = boto3.Session(region_name=cur_region)

from autoscaling import AutoScalingGroup

resource_session = session.resource('ec2')
client_session = session.client('ec2')
client = boto3.client('autoscaling')
route53_session = session.client('route53')
elb_session = session.client('elb')

# Class default variables for staging env.
auto_scaling = AutoScalingGroup('session')
auto_scaling.default_image_id = default_image
auto_scaling.default_instance_type = default_inst_type
user_data_file = '/Users/sunahmad/bootstrap_staging.py'
fh = open(user_data_file)
aws_stalk_info = {}


def get_available_vpcs():
    vpc_list = []
    client = boto3.client('ec2')
    all_vpcs = client.describe_vpcs()
    if len(all_vpcs['Vpcs']) > 0:
        for x in range(len(all_vpcs['Vpcs'])):
            vpc_list.append(all_vpcs['Vpcs'][x]['Tags'][0]['Value'])
    return vpc_list


def get_load_balancer():
    elb_list = []
    client = boto3.client('elb')
    elb = client.describe_load_balancers()
    if len(elb) > 0:
        for x in range(len(elb['LoadBalancerDescriptions'])):
            elb_list.append(elb['LoadBalancerDescriptions'][x]['LoadBalancerName'])
    return elb_list


def get_launch_config():
    lc_list = []
    client = boto3.client('autoscaling')
    lc = client.describe_launch_configurations()
    if len(lc) > 0:
        for x in range(len(lc['LaunchConfigurations'])):
            lc_list.append(lc['LaunchConfigurations'][x]['LaunchConfigurationName'])
    return lc_list


def get_auto_scaling_groups():
    as_list = []
    client = boto3.client('autoscaling')
    auto_config = client.describe_auto_scaling_groups()
    if len(auto_config) > 0:
        for x in range(len(auto_config['AutoScalingGroups'])):
            as_list.append(auto_config['AutoScalingGroups'][x]['AutoScalingGroupName'])
    return as_list


def tag_exists(tag, lc_list):
    if tag in lc_list:
        print "already exists!", tag
        return True
    else:
        print "%s does not exists! existing %s " % (tag, lc_list)
        return False

if results.environment:
    env_name = results.environment
else:
    env_name = 'staging'

micro_service_name = results.service_name + '-' + env_name
auto_scaling.default_tags = micro_service_name

if not tag_exists(micro_service_name, get_load_balancer()):
    elb = auto_scaling.create_elb(
            subnets=['subnet-9430f8cc', 'subnet-f7840481', 'subnet-e9056c8d'],
            elb_port=443, security_group=['sg-9da8cefb'], in_port=80,
            elb_name=micro_service_name, listeners_protocol='https')
else:
    print "elb already exits: %s" % micro_service_name
    sys.exit()

if not tag_exists(micro_service_name, get_auto_scaling_groups()):
    scaling_group = auto_scaling.create_auto_scaling(
            min=1, max=2, lc_name='close5-api-staging', as_name=micro_service_name, elb_name=micro_service_name,
            instance_tags=results.service_name, vpcz_id='subnet-9330f8cb, subnet-f4840482')
else:
    print "auto scaling group already exists: %s" % micro_service_name
    sys.exit()

micro_server_up_policy = auto_scaling.put_scaling_policy(
        scaling_adjustment=1, as_name=micro_service_name,
        policy_name= micro_service_name + ' scaling up')
print micro_server_up_policy

micro_server_down_policy = auto_scaling.put_scaling_policy(
        scaling_adjustment=-1, as_name=micro_service_name,
        policy_name=micro_service_name + ' scaling down')
print micro_server_down_policy

micro_service_scale_up_metric_alarm = auto_scaling.put_metric_alarm(
        alarm_name=micro_service_name + " scaling up", as_name=micro_service_name,
        alarm_actions=[micro_server_up_policy['PolicyARN']], threshold=60)
print micro_service_scale_up_metric_alarm

micro_service_scale_down_metric_alarm = auto_scaling.put_metric_alarm(
        alarm_name=micro_service_name + " scaling down", as_name=micro_service_name,
        alarm_description='scaling down polity', alarm_actions=[micro_server_down_policy['PolicyARN']],
        comparison_operator='LessThanOrEqualToThreshold', threshold=40)
print micro_service_scale_up_metric_alarm

elb = elb_session.describe_load_balancers(LoadBalancerNames=[micro_service_name])
elb_dnsname = elb['LoadBalancerDescriptions'][0]['DNSName']
elb_ms_name = 'elb-' + micro_service_name + '.staging2.close5.com'

response = route53_session.change_resource_record_sets(
        HostedZoneId = 'ZQ1NS2BHEW1QI',
        ChangeBatch={
            'Comment': 'comment',
            'Changes': [
                {
                    'Action': 'CREATE',
                    'ResourceRecordSet': {
                        'Name': elb_ms_name,
                        'Type': 'CNAME',
                        'SetIdentifier': 'staging',
                        'GeoLocation': {},
                        'TTL': 60,
                        'ResourceRecords': [
                            {
                                'Value': elb_dnsname
                            },
                        ],
                    }
                },
            ]
        }
)
print("DNS CNAME/Endpoint for the Micro Service: %s " % elb_ms_name)