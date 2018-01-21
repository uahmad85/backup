#!/usr/bin/env python

from fabric import
from time import sleep
from fabric.api import execute, run, sudo, env
import boto3
import os

if os.environ.get('host_name'):
    hosts = os.environ.get('host_name')
    if ',' in hosts:
        for host in hosts.split(','):
            env.hosts.append(host)
    else:
        env.hosts.append(hosts)

if os.environ.get('service_name'):
    service_name = env.service_name

env.user = 'ubuntu'
env.key_filename = '/var/lib/jenkins/.ssh/close5-lnp.pem'


def aws_vpc_region(vpcid, region='us-west-2'):
    aws = {}
    aws['aws_region'] = "%s" % region
    aws['vpc'] = "%s" % vpcid
    print "\nAWS_REGION: %s - AWS_VPC: %s" % (aws['aws_region'], aws['vpc'])
    return aws

aws = aws_vpc_region(vpcid=env.vpcid)
session = boto3.Session(region_name=aws['aws_region'])


def get_private_ips(itag, vpcid=aws['vpc']):
    ip_list = []
    client = session.resource('ec2')
    vpc = client.Vpc(vpcid)
    instances = vpc.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': [itag]}])
    print "----"
    for x in range(len(list(instances))):
        instance = client.Instance(list(instances)[x].id)
        ip_list.append(instance.private_ip_address)
    print "Chef client will run on %s host(s)!\nMicro Service Name: %s" % (len(ip_list), instance.tags[0]['Value'])
    return ip_list
    sleep(1)

# for testing
###############
def host_type():
    run('uname -s')


def run_sudo_check():
    sudo("hostname")
###############

def run_chef_client():
    """ Chef client run will pull all the changes from git and chef-server """
    sudo("chef-client")


def check_git_branch():
    sudo("cd /opt/close5/core-api; git branch")


def deploy(tag):
    execute(run_chef_client, hosts=get_private_ips(itag=tag))


def tail_logs_200():
    sudo("tail -n 200 /var/log/%s.log" % service_name)