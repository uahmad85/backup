#!/usr/bin/env python
import boto3
import sys
import os
from ConfigParser import SafeConfigParser
from time import sleep
import argparse
import json

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

print cur_region

session = boto3.Session(region_name=cur_region)

from tag_resources import ResTags
from autoscaling import AutoScalingGroup

resource_session = session.resource('ec2')
client_session = session.client('ec2')
client = boto3.client('autoscaling')
boto3.set_stream_logger('botocore')

# Class default variables for lnp env.
auto_scaling = AutoScalingGroup('session')
auto_scaling.default_tags = 'core-api'
auto_scaling.default_image_id = 'ami-c9887ba9'
auto_scaling.default_instance_type = 'c3.xlarge'

user_data_file = '/Users/sunahmad/bootstrap.py'
fh = open(user_data_file)
aws_stalk_info = {}


def elb_exists(tag):
    client = boto3.client('elb')
    elb = client.describe_load_balancers()
    for x in range(len(elb['LoadBalancerDescriptions'])):
        if tag == elb['LoadBalancerDescriptions'][x]['LoadBalancerName']:

            return True

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
                                                            comparison_operator='LessThanOrEqualToThreshold', threshold=10)
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

frontend_vlans = ['10.0.21.0/24', '10.0.41.0/24']
backend_vlans = ['10.0.31.0/24', '10.0.51.0/24']
pri_zones = ['us-west-2b', 'us-west-2c']

def tags(value=None):
    Tags=[
        {'Key': 'Name',
         'Value': value}
    ]
    return Tags

print "     AWS Region: ", cur_region


def create_vpc(resource_session, dryrun=True):
    vpc = resource_session.create_vpc(DryRun=dryrun,
                                      CidrBlock='10.0.0.0/16',
                                      InstanceTenancy='default')
    return vpc

vpc = create_vpc(resource_session, dryrun=False)
vpc_id = [vpc][0].id
waiter = client_session.get_waiter('vpc_available')
waiter.wait(DryRun=False, VpcIds=[vpc_id])

tag_vpc = ResTags(resource_session).tag_vpc(False, vpc_id, tags('close5-' + results.environment))
vpc_con = resource_session.Vpc(vpc_id)
sg_list = list(vpc_con.security_groups.all())
default_sg = sg_list[0].id

tag_sg = ResTags(resource_session).tag_securitygroup(False, default_sg, tags('default for all the instances'))
print tag_sg
print tag_vpc


def get_availability_zones(client_session):
    az_list = []
    zones = client_session.describe_availability_zones()
    for zone in zones['AvailabilityZones']:
        az_list.append(zone['ZoneName'])
    return az_list

avail_zones = get_availability_zones(client_session)
print "Availability Zones: ", avail_zones


def mk_subnet(resource_session, vpcid, dryrun=True, cidrblk='10.0.11.0/24', az='us-west-2a'):
    subnet = resource_session.create_subnet(DryRun=dryrun, VpcId=vpcid,
                                                CidrBlock=cidrblk, AvailabilityZone=az)
    return subnet

pub_sub = mk_subnet(resource_session, vpc_id, False)
pub_sub_id = [pub_sub][0].id

for index in range(len(pri_zones)):
    subnets = mk_subnet(resource_session, vpc_id, False, frontend_vlans[index], az=pri_zones[index])


for index in range(len(pri_zones)):
    xsubnets = mk_subnet(resource_session, vpc_id, False, backend_vlans[index], az=pri_zones[index])


def filter_subnets(key, value):
    response = client_session.describe_subnets(DryRun=False, Filters=[{"Name": key, "Values": [value]}])
    return response['Subnets'][0]['SubnetId']

vpc_con = resource_session.Vpc(vpc_id)
subnets_list = list(vpc_con.subnets.all())
print "available subnets: %s" % subnets_list


def get_sub_id_from_tag(tag=None):
    for x in range(len(subnets_list)):
        sub = resource_session.Subnet(subnets_list[x].id)
        if sub.tags[0]['Value'] == tag:
            return sub.subnet_id


pri_only_subnets = []
for x in range(len(subnets_list)):
    if subnets_list[x].id != pub_sub_id:
        pri_only_subnets.append(subnets_list[x].id)

print pri_only_subnets, len(pri_only_subnets)
print ResTags(resource_session).tag_subnet(False, pub_sub_id, tags('public01'))

subnet_tags = [ 'private01', 'private02', 'private03', 'private04']

for x in range(len(pri_only_subnets)):
    print ResTags(resource_session).tag_subnet(False, pri_only_subnets[x], tags(subnet_tags[x]))
    sleep(1)

internet_gateway = resource_session.create_internet_gateway()
internet_gateway_id = [internet_gateway][0].id
sleep(2)
tag_ig = ResTags(resource_session).tag_internetgateway(False, [internet_gateway][0].id, tags('InternetGateway'))
print tag_ig


def attach_ig(vpc_con, igid):
    response = vpc_con.attach_internet_gateway(DryRun=False,
                                               InternetGatewayId=igid)
    return response

print attach_ig(vpc_con, internet_gateway_id)


def create_routetable(vpcid, resource_session=resource_session):
    routetable = resource_session.create_route_table(VpcId=vpcid)
    return routetable

table_id = create_routetable(vpc_id)
tag_rt = ResTags(resource_session).tag_routetable(False, [table_id][0].id, tags('RouteTable with InternetGateway'))
print tag_rt


def create_route(rt_id, cidrblock='0.0.0.0/0', igid=internet_gateway_id):
    route = resource_session.RouteTable(rt_id)
    ig_route = route.create_route(DestinationCidrBlock=cidrblock, GatewayId=igid)
    return ig_route

print create_route([table_id][0].id)


def associate_with_subnet(table_id, subnetid):
    routetable = resource_session.RouteTable(table_id)
    response = routetable.associate_with_subnet(SubnetId=subnetid)
    return response

for subnets in ['public01']:
    print associate_with_subnet([table_id][0].id, pub_sub_id)


def create_security_group(vpc_con, group_name=None, description='Security Group for DB instances'):
    sg = vpc_con.create_security_group(GroupName=group_name,
                                       Description=description)
    return sg

nat_sg = create_security_group(vpc_con, group_name='close5-dev-nat')
nat_sgid = [nat_sg][0].id

mongodb_sg = create_security_group(vpc_con, group_name='mongodb', description='mongodb security group')
mongodb_sg_id = [mongodb_sg][0].id


sleep(1)

tag_nat_sg = ResTags(resource_session).tag_securitygroup(False, nat_sgid, tags('nat security group for DBs'))
tag_mongodb_sg = ResTags(resource_session).tag_securitygroup(False, mongodb_sg_id, tags('DBs security group'))
print tag_nat_sg
print tag_mongodb_sg


def create_ingress_rules(resource_session, sgid=nat_sgid, from_port=80, to_port=80, cidr='0.0.0.0/0'):
    sg = resource_session.SecurityGroup(sgid)
    reponse = sg.authorize_ingress(IpProtocol="tcp", FromPort=from_port, ToPort=to_port, CidrIp=cidr)
    return reponse

http_rule = create_ingress_rules(resource_session, cidr='10.0.0.0/24')
https_rule = create_ingress_rules(resource_session, from_port=443, to_port=443, cidr='10.0.0.0/24')
mongo_rule = create_ingress_rules(resource_session, sgid=mongodb_sg_id, from_port=27017, to_port=27017, cidr='10.0.0.0/24')

# creating instances and setting up configurable items.
if results.image:
    default_image = results.image

if results.instance_type:
    default_inst_type = results.instance_type

if results.number_of_instances:
    maxcount = results.number_of_instances


def create_instance(subnet_id, inst_type, resource_session=resource_session, dryrun=False,
                    image_id='ami-9abea4fb', maxcount=1, sshkey='close5-lnp', instance_sg='default', public_ip=False):
    instance = resource_session.create_instances(DryRun=dryrun, ImageId=image_id, MinCount=1, UserData=fh.read(),
                                                 MaxCount=maxcount, KeyName=sshkey, InstanceType=inst_type,
                                                 NetworkInterfaces=[{'DeviceIndex': 0, 'SubnetId': subnet_id,
                                                                     'Groups': [instance_sg],
                                                                     'AssociatePublicIpAddress': public_ip}])
    return instance
nat_instance = create_instance(image_id='ami-030f4133', inst_type='t1.micro',
                               subnet_id=get_sub_id_from_tag("public01"),
                               instance_sg=nat_sgid, public_ip=True)

nat_instance_id = nat_instance[0].id
waiter = client_session.get_waiter('instance_running')
waiter.wait(DryRun=False, InstanceIds=[nat_instance_id])


def get_network_ifc_id(resource_session=resource_session,
                       nat_instance_id=nat_instance_id):
    instance = resource_session.Instance(nat_instance_id)
    all_attri = instance.network_interfaces_attribute
    for eni_id in all_attri:
        return eni_id['NetworkInterfaceId']

eni = get_network_ifc_id()
response = client_session.modify_network_interface_attribute(NetworkInterfaceId=eni,
                                                             SourceDestCheck={'Value': False})
print response

tag_nat_inst = ResTags(resource_session).tag_instance(False, nat_instance_id, tags('nat-instance'))
print tag_nat_inst

nat_table = create_routetable(vpc_id)
nat_table_id = [nat_table][0].id
sleep(1)
nat_tag_rt = ResTags(resource_session).tag_routetable(False, nat_table_id, tags('RouteTable with NatGateway'))
print nat_tag_rt


def create_route(rt_id, nat_inst_id, cidrblock='0.0.0.0/0'):
    route = resource_session.RouteTable(rt_id)
    ig_route = route.create_route(DestinationCidrBlock=cidrblock, RouteTableId=nat_table_id,
                                  InstanceId=nat_inst_id)
    return ig_route

print create_route(nat_table_id, nat_instance_id)

for subnets in pri_only_subnets:
    print associate_with_subnet(nat_table_id, subnets)

com_tags = [tags('core-api'), tags('images-server'), tags('consumer'), tags('elasticsearch')]

if results.environment == 'development':
    instance_pub = create_instance(inst_type='t2.micro', subnet_id=get_sub_id_from_tag('private01'),
                                   maxcount=4, instance_sg=default_sg, public_ip=False)
    instance_pri = create_instance(inst_type='t2.micro', subnet_id=get_sub_id_from_tag('private02'),
                                   maxcount=3, instance_sg=mongodb_sg_id, public_ip=False)
    try:
        for x in range(len(instance_pub)):
            waiter.wait(DryRun=False, InstanceIds=[instance_pub[x].id])
            tag_pub_inst = ResTags(resource_session).tag_instance(False, instance_pub[x].id, com_tags[x])
            print tag_pub_inst
    except:
        err = sys.exc_info()
        print "ERR MSG: " + str(err[1])

    try:
        for x in range(len(instance_pri)):
            waiter.wait(DryRun=False, InstanceIds=[instance_pri[x].id])
            tag_pri_inst = ResTags(resource_session).tag_instance(False, instance_pri[x].id, tags('mongodb0' + str(x)))
            print tag_pri_inst
    except:
        err = sys.exc_info()
        print "ERR MSG: " + str(err[1])


if results.environment == 'staging':
    auto_scaling.default_tags = 'staging-api'
    auto_scaling.default_lc_name = 'close5-staging'
    auto_scaling.default_instance_type = 'c3.xlarge'

    if not elb_exists(auto_scaling.default_tags):
        elb = auto_scaling.create_elb(subnets=subnets_list, elb_port=443,
                                      in_port=9000, elb_name=auto_scaling.default_tags)
    sleep(2)
    core_api_sg = create_security_group(vpc_con, group_name=auto_scaling.default_tags, description='core-api security group')
    core_api_sg_id = [core_api_sg][0].id
    core_api_rules_80 = create_ingress_rules(resource_session, sgid=core_api_sg_id, from_port=9000, to_port=9000, cidr='10.0.0.0/24')
    core_api_rules_443 = create_ingress_rules(resource_session, sgid=core_api_sg_id, from_port=9000, to_port=9000, cidr='172.31.0.0/16')
    core_api_rules_443 = create_ingress_rules(resource_session, sgid=core_api_sg_id, from_port=9000, to_port=9000, cidr='10.0.0.0/24')
    core_api_rules_elb = create_ingress_rules(resource_session, sgid=core_api_sg_id, from_port=9000, to_port=9000, cidr='172.31.0.0/16')
    core_api_rules_80 = create_ingress_rules(resource_session, sgid=core_api_sg_id, from_port=80, to_port=80, cidr='10.0.0.0/24')
    core_api_rules_443 = create_ingress_rules(resource_session, sgid=core_api_sg_id, from_port=80, to_port=80, cidr='172.31.0.0/16')
    core_api_rules_443 = create_ingress_rules(resource_session, sgid=core_api_sg_id, from_port=443, to_port=443, cidr='10.0.0.0/24')
    core_api_rules_elb = create_ingress_rules(resource_session, sgid=core_api_sg_id, from_port=443, to_port=443, cidr='172.31.0.0/16')

    des_la_cfg = client.describe_launch_configurations()
    if not des_la_cfg['LaunchConfigurations']:
        lunch_config = auto_scaling.create_launch_config(security_group=[core_api_sg_id])
    elif des_la_cfg['LaunchConfigurations'][0]['LaunchConfigurationName'] != "close5-staging":
        lunch_config = auto_scaling.create_launch_config(security_group=[core_api_sg_id])
        print lunch_config

    scaling_group = auto_scaling.create_auto_scaling(min=1, max=3, vpcz_id=', '.join([get_sub_id_from_tag('private01'),
                                                                                      get_sub_id_from_tag('private03')]))
    print scaling_group

    scaling_up_policy = auto_scaling.put_scaling_policy(scaling_adjustment=1)
    print scaling_up_policy

    scaling_down_policy = auto_scaling.put_scaling_policy(scaling_adjustment=-1, policy_name='scaling down')
    print scaling_down_policy

    scale_up_metric_alarm = auto_scaling.put_metric_alarm(alarm_name="scaling up", threshold=40,
                                                          alarm_actions=[scaling_up_policy['PolicyARN']])
    print scale_up_metric_alarm

    scale_down_metric_alarm = auto_scaling.put_metric_alarm(alarm_name="scaling down",
                                                            alarm_description='scaling down polity',
                                                            alarm_actions=[scaling_down_policy['PolicyARN']],
                                                            comparison_operator='LessThanOrEqualToThreshold', threshold=10)
    print scale_down_metric_alarm

    sleep(3)
    ######   images-server setup   ##########
    sleep(3)

    auto_scaling.default_tags = 'staging-images-server'

    if not elb_exists(auto_scaling.default_tags):
        elb = auto_scaling.create_elb(subnets=subnets_list, elb_port=443,
                                      in_port=80, elb_name=auto_scaling.default_tags)
    images_server_sg = create_security_group(vpc_con, group_name='mongodb', description='images security group')
    images_server_sg_id = [images_server_sg][0].id
    sleep(2)
    images_server_rules_80 = create_ingress_rules(resource_session, sgid=images_server_sg_id, from_port=80, to_port=80, cidr='10.0.0.0/24')
    images_server_rules_443 = create_ingress_rules(resource_session, sgid=images_server_sg_id, from_port=80, to_port=80, cidr='172.31.0.0/16')
    images_server_rules_443 = create_ingress_rules(resource_session, sgid=images_server_sg_id, from_port=443, to_port=80, cidr='10.0.0.0/24')
    images_server_rules_elb = create_ingress_rules(resource_session, sgid=images_server_sg_id, from_port=443, to_port=80, cidr='172.31.0.0/16')

    des_la_cfg = client.describe_launch_configurations()
    if not des_la_cfg['LaunchConfigurations']:
        lunch_config = auto_scaling.create_launch_config(security_group=[images_server_sg_id])
    elif des_la_cfg['LaunchConfigurations'][0]['LaunchConfigurationName'] != "close5-staging":
        lunch_config = auto_scaling.create_launch_config([images_server_sg_id])
        print lunch_config

    scaling_group = auto_scaling.create_auto_scaling(min=1, max=3, vpcz_id=', '.join([get_sub_id_from_tag('private01'),
                                                                                      get_sub_id_from_tag('private03')]))
    print scaling_group

    scaling_group = auto_scaling.create_auto_scaling(min=1, max=3, lc_name=auto_scaling.default_lc_name)
    print scaling_group

    images_scaling_up_policy = auto_scaling.put_scaling_policy(scaling_adjustment=1,
                                                               policy_name='staging images scaling up')
    print images_scaling_up_policy

    images_scaling_down_policy = auto_scaling.put_scaling_policy(scaling_adjustment=-1,
                                                                 policy_name='staging images scaling down')
    print images_scaling_down_policy

    images_scale_up_metric_alarm = auto_scaling.put_metric_alarm(alarm_name="images scaling up",
                                                                 alarm_actions=[images_scaling_up_policy['PolicyARN']],
                                                                 threshold=60)
    print images_scale_up_metric_alarm

    images_scale_down_metric_alarm = auto_scaling.put_metric_alarm(alarm_name='images scaling down',
                                                                   alarm_description='scaling down polity',
                                                                   alarm_actions=[images_scaling_down_policy['PolicyARN']],
                                                                   comparison_operator='LessThanOrEqualToThreshold',
                                                                   threshold=40)
    print images_scale_down_metric_alarm
    sleep(3)
    ######   images-server setup   ##########
    sleep(3)

    auto_scaling.default_tags = 'staging-consumer'

    if not elb_exists(auto_scaling.default_tags):
        elb = auto_scaling.create_elb(subnets=subnets_list, elb_port=443,
                                      in_port=80, elb_name=auto_scaling.default_tags)

    consumer_sg = create_security_group(vpc_con, group_name='consumer', description='consumer security group')
    consumer_sg_id = [core_api_sg][0].id
    sleep(2)
    consumer_rules_80 = create_ingress_rules(resource_session, sgid=consumer_sg_id, from_port=80, to_port=80, cidr='10.0.0.0/24')
    consumer_rules_443 = create_ingress_rules(resource_session, sgid=consumer_sg_id, from_port=80, to_port=80, cidr='172.31.0.0/16')
    consumer_rules_443 = create_ingress_rules(resource_session, sgid=consumer_sg_id, from_port=443, to_port=80, cidr='10.0.0.0/24')
    consumer_rules_elb = create_ingress_rules(resource_session, sgid=consumer_sg_id, from_port=443, to_port=80, cidr='172.31.0.0/16')

    des_la_cfg = client.describe_launch_configurations()
    if not des_la_cfg['LaunchConfigurations']:
        lunch_config = auto_scaling.create_launch_config(security_group=[images_server_sg_id])
    elif des_la_cfg['LaunchConfigurations'][0]['LaunchConfigurationName'] != "close5-staging":
        lunch_config = auto_scaling.create_launch_config([images_server_sg_id])
        print lunch_config

    scaling_group = auto_scaling.create_auto_scaling(min=1, max=3, vpcz_id=', '.join([get_sub_id_from_tag('private01'),
                                                                                      get_sub_id_from_tag('private03')]))
    print scaling_group

    consumer_scaling_up_policy = auto_scaling.put_scaling_policy(scaling_adjustment=1,
                                                                 policy_name='staging consumer scaling up')
    print consumer_scaling_up_policy

    consumer_scaling_down_policy = auto_scaling.put_scaling_policy(scaling_adjustment=-1,
                                                                   policy_name='staging consumer scaling down')
    print consumer_scaling_down_policy

    consumer_scale_up_metric_alarm = auto_scaling.put_metric_alarm(alarm_name="consumer scaling up",
                                                                   alarm_actions=[consumer_scaling_up_policy['PolicyARN']])
    print consumer_scale_up_metric_alarm

    consumer_scale_down_metric_alarm = auto_scaling.put_metric_alarm(alarm_name='consumer scaling down',
                                                                     alarm_description='scaling down polity',
                                                                     alarm_actions=[consumer_scaling_down_policy['PolicyARN']],
                                                                     comparison_operator='LessThanOrEqualToThreshold',
                                                                     threshold=30)
    print consumer_scale_down_metric_alarm
    sys.exit()


#aws_stalk_info['vpc'] = {}
#aws_stalk_info['vpc']['vpc_info'] = '%s' % vpc
#aws_stalk_info['vpc']['default_sg'] = '%s' % tag_sg
#aws_stalk_info['vpc']['available_azs'] = '%s' % avail_zones
#aws_stalk_info['vpc']['subnets'] = '%s' % subnets
##aws_stalk_info['vpc']['subnets_tags1'] = '%s' % pub_sub01
##aws_stalk_info['vpc']['subnets_tags2'] = '%s' % pub_sub02
#aws_stalk_info['vpc']['subnets_tags3'] = '%s' % pri_sub01
#aws_stalk_info['vpc']['internetgateway'] = '%s' % tag_ig
#aws_stalk_info['vpc']['routetable'] = '%s' % tag_rt
#aws_stalk_info['vpc']['nat_security_group'] = '%s' % tag_nat_sg
#aws_stalk_info['vpc']['nat_security_group_rules'] = {}
#aws_stalk_info['vpc']['nat_security_group_rules'] = '%s' % http_rule
#aws_stalk_info['vpc']['nat_security_group_rules'] = '%s' % https_rule
#aws_stalk_info['vpc']['nat_security_group_rules'] = '%s' % ssh_rule
#aws_stalk_info['vpc']['instances'] = {}
#aws_stalk_info['vpc']['instances']['nat_instance'] = '%s' % tag_nat_inst
#aws_stalk_info['vpc']['instances']['pub_instances'] = '%s' % tag_pub_inst
#aws_stalk_info['vpc']['instances']['pri_instances'] = '%s' % tag_pri_inst

#data_file_path = os.getcwd()
#data_file = data_file_path + '/' + 'aws_stalk_info'
#print aws_stalk_info
#fh = open(aws_stalk_info, 'w')
#json.dump(str(aws_stalk_info), fh)