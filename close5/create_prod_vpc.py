#!/usr/bin/env python
import boto3
import sys
import os
from ConfigParser import SafeConfigParser
from time import sleep
import argparse
import json

default_vpc = 'vpc-48739c2c'
userId = '712818841314'
default_image = 'ami-030f4133'
default_inst_type = 't1.micro'

parser = argparse.ArgumentParser(description='Usage: create_env.py -e <environment> -r <region>')
parser.add_argument('-i', '--image', action='store', help='Image Id to be use, default is ' + default_image)
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

from tag_resources import ResTags
from autoscaling import AutoScalingGroup

resource_session = session.resource('ec2')
client_session = session.client('ec2')
client = boto3.client('autoscaling')
route53_session = session.client('route53')

# Class default variables for lnp env.
auto_scaling = AutoScalingGroup('session')
auto_scaling.default_tags = 'core-api'
auto_scaling.default_image_id = 'ami-c9887ba9'
auto_scaling.default_instance_type = 'c3.xlarge'

user_data_file = '/Users/sunahmad/bootstrap.py'
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
        return True
    else:
        print "%s does not exists! existing %s " % (tag, lc_list)
        return False

if results.environment == 'production':
    des_la_cfg = client.describe_launch_configurations()
    if not des_la_cfg['LaunchConfigurations']:
        lunch_config = auto_scaling.create_launch_config()
    elif des_la_cfg['LaunchConfigurations'][0]['LaunchConfigurationName'] != "core-api":
        lunch_config = auto_scaling.create_launch_config()
        print lunch_config

    scaling_group = auto_scaling.create_auto_scaling(min=3, max=10)
    print scaling_group

    scaling_up_policy = auto_scaling.put_scaling_policy(scaling_adjustment=1)
    print scaling_up_policy

    scaling_down_policy = auto_scaling.put_scaling_policy(scaling_adjustment=-1, policy_name='scaling down')
    print scaling_down_policy

    scale_up_metric_alarm = auto_scaling.put_metric_alarm(as_name='core-api', alarm_name="scaling up",
                                                          alarm_actions=[scaling_up_policy['PolicyARN']], threshold=40)
    print scale_up_metric_alarm

    scale_down_metric_alarm = auto_scaling.put_metric_alarm(as_name='core-api', alarm_name="scaling down",
                                                            alarm_description='scaling down polity',
                                                            alarm_actions=[scaling_down_policy['PolicyARN']],
                                                            comparison_operator='LessThanOrEqualToThreshold',
                                                            threshold=10)
    print scale_down_metric_alarm

    sleep(3)
    ######   images-server setup   ##########
    sleep(3)

    auto_scaling.default_tags = 'images-server'
    auto_scaling.default_instance_type = 'm3.2xlarge'

    scaling_group = auto_scaling.create_auto_scaling(min=2, max=25)
    print scaling_group

    images_scaling_up_policy = auto_scaling.put_scaling_policy(scaling_adjustment=1, policy_name='images scaling up')
    print images_scaling_up_policy

    images_scaling_down_policy = auto_scaling.put_scaling_policy(scaling_adjustment=-1, policy_name='images scaling down')
    print images_scaling_down_policy

    images_scale_up_metric_alarm = auto_scaling.put_metric_alarm(as_name='images-server', alarm_name="images scaling up",
                                                                 alarm_actions=[images_scaling_up_policy['PolicyARN']],
                                                                 threshold=60)
    print images_scale_up_metric_alarm

    images_scale_down_metric_alarm = auto_scaling.put_metric_alarm(as_name='images-server', alarm_name='images scaling down',
                                                                   alarm_description='scaling down polity',
                                                                   alarm_actions=[images_scaling_down_policy['PolicyARN']],
                                                                   comparison_operator='LessThanOrEqualToThreshold',
                                                                   threshold=40)
    print images_scale_down_metric_alarm
    sleep(3)
    ######   images-server setup   ##########
    sleep(3)

    auto_scaling.default_tags = 'consumer'

    scaling_group = auto_scaling.create_auto_scaling(min=3, max=20)
    print scaling_group

    consumer_scaling_up_policy = auto_scaling.put_scaling_policy(scaling_adjustment=1, policy_name='consumer scaling up')
    print consumer_scaling_up_policy

    consumer_scaling_down_policy = auto_scaling.put_scaling_policy(scaling_adjustment=-1, policy_name='consumer scaling down')
    print consumer_scaling_down_policy

    consumer_scale_up_metric_alarm = auto_scaling.put_metric_alarm(as_name='consumer', alarm_name="consumer scaling up",
                                                                   alarm_actions=[consumer_scaling_up_policy['PolicyARN']])
    print consumer_scale_up_metric_alarm

    consumer_scale_down_metric_alarm = auto_scaling.put_metric_alarm(as_name='consumer', alarm_name='consumer scaling down',
                                                                     alarm_description='scaling down polity',
                                                                     alarm_actions=[consumer_scaling_down_policy['PolicyARN']],
                                                                     comparison_operator='LessThanOrEqualToThreshold',
                                                                     threshold=30)
    print consumer_scale_down_metric_alarm
    sys.exit()
