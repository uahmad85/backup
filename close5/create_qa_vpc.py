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
default_image = 'ami-78aa7f18'
nat_image = 'ami-030f4133'
default_inst_type = 't1.micro'
squid_image = 'ami-2c6d914c'
node_image = 'ami-78aa7f18'


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

user_data_file = '/Users/sunahmad/bootstrap_production.py'
fh = open(user_data_file)
aws_stalk_info = {}


def get_available_vpcs():
    vpc_list = []
    client = boto3.client('ec2')
    all_vpcs = client.describe_vpcs()
    if len(all_vpcs['Vpcs']) > 0:
        for x in range(len(all_vpcs['Vpcs'])):
            if all_vpcs['Vpcs'][x]['Tags']:
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

frontend_vlans = ['10.100.3.0/24', '10.100.5.0/24']
backend_vlans = ['10.100.4.0/24', '10.100.6.0/24']

all_vlans = frontend_vlans + backend_vlans

pri_zones = ['us-west-1a', 'us-west-1c']
environment_name = 'close5-' + results.environment

print "\tAWS Region: ", cur_region
if tag_exists(environment_name, get_available_vpcs()):
    print "\nVpc already exists '%s'. However, if you want to create a new VPC please use a different " \
          "environment name {dev|staging|qa|lnp}" % environment_name
    sys.exit()


def tags(value=None):
    Tags=[
        {'Key': 'Name',
         'Value': value}
    ]
    return Tags

print "\tAWS Region: ", cur_region


def create_vpc(resource_session, dryrun=True):
    vpc = resource_session.create_vpc(DryRun=dryrun,
                                      CidrBlock='10.100.0.0/16',
                                      InstanceTenancy='default')
    return vpc

vpc = create_vpc(resource_session, dryrun=False)
vpc_id = [vpc][0].id
vpc_con = resource_session.Vpc(vpc_id)

waiter = client_session.get_waiter('vpc_available')
waiter.wait(DryRun=False, VpcIds=[vpc_id])

sg_list = list(vpc_con.security_groups.all())
default_sg = sg_list[0].id

tag_vpc = ResTags(resource_session).tag_vpc(False, vpc_id, tags('close5-' + results.environment))
tag_sg = ResTags(resource_session).tag_securitygroup(False, default_sg, tags('default for all the instances'))
print tag_sg
print tag_vpc

enable_dns_res = vpc_con.modify_attribute(EnableDnsHostnames={'Value': True})

associate_vpc_with_zone = route53_session.associate_vpc_with_hosted_zone(HostedZoneId='Z3OL1G88U963Q0',
                                                                         VPC={'VPCRegion': 'us-west-2',
                                                                              'VPCId': vpc_id})


def get_availability_zones(client_session):
    az_list = []
    zones = client_session.describe_availability_zones()
    for zone in zones['AvailabilityZones']:
        az_list.append(zone['ZoneName'])
    return az_list

avail_zones = get_availability_zones(client_session)
print "Availability Zones: ", avail_zones


def mk_subnet(resource_session, vpcid, dryrun=True, cidrblk='10.100.1.0/24', az='us-west-1a'):
    subnet = resource_session.create_subnet(DryRun=dryrun, VpcId=vpcid,
                                            CidrBlock=cidrblk, AvailabilityZone=az)
    return subnet

pub_sub01 = mk_subnet(resource_session, vpc_id, False)
pub_sub_id01 = [pub_sub01][0].id

pub_sub02 = mk_subnet(resource_session, vpc_id, False, cidrblk='10.100.2.0/24', az='us-west-1c')
pub_sub_id02 = [pub_sub02][0].id

for index in range(len(frontend_vlans)):
    pub_subnets = mk_subnet(resource_session, vpc_id, False, cidrblk=frontend_vlans[index], az='us-west-1a')

for index in range(len(backend_vlans)):
    pri_subnets = mk_subnet(resource_session, vpc_id, False, cidrblk=backend_vlans[index], az='us-west-1c')


def filter_subnets(key, value):
    response = client_session.describe_subnets(DryRun=False, Filters=[{"Name": key, "Values": [value]}])
    return response['Subnets'][0]['SubnetId']

vpc_con = resource_session.Vpc(vpc_id)
subnets_list = list(vpc_con.subnets.all())
print "available subnets: %s" % subnets_list


def security_group_exists(vpc_con=vpc_con, tag=None):
    for i in vpc_con.security_groups.filter(Filters=[{"Name": "group-name", "Values": [tag]}]):
        if i == "":
            return False
        else:
            print "security group already exists: {0}".format(resource_session.SecurityGroup([i][0].id).tags[0]['Value'])
            return True


def get_sub_id_from_tag(tag=None):
    for x in range(len(subnets_list)):
        sub = resource_session.Subnet(subnets_list[x].id)
        if sub.tags[0]['Value'] == tag:
            return sub.subnet_id


def get_sub_az(az, subnets_list):
    for ids in subnets_list:
        subnet = resource_session.Subnet(ids)
        if subnet.availability_zone == az:
            return ids


pub_only_subnets = [pub_sub_id01, pub_sub_id02]
pri_only_subnets = []

for x in range(len(subnets_list)):
    if subnets_list[x].id not in pub_only_subnets:
        pri_only_subnets.append(subnets_list[x].id)

print pri_only_subnets, len(pri_only_subnets)
print ResTags(resource_session).tag_subnet(False, pub_sub_id01, tags('public01'))
print ResTags(resource_session).tag_subnet(False, pub_sub_id02, tags('public02'))

pri_subnet_tags = ['private01', 'private02', 'private03', 'private04']

for x in range(len(pri_only_subnets)):
    print ResTags(resource_session).tag_subnet(False, pri_only_subnets[x], tags(pri_subnet_tags[x]))
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

for x in range(1):
    print associate_with_subnet([table_id][0].id, get_sub_id_from_tag('public01'))
    print associate_with_subnet([table_id][0].id, get_sub_id_from_tag('public02'))


def create_security_group(vpc_con, group_name=None, description='Security Group for DB instances'):
    sg = vpc_con.create_security_group(GroupName=group_name,
                                       Description=description)
    return sg
nat_sg_name = 'close5-prod-nat'
nat_sg = create_security_group(vpc_con, group_name=nat_sg_name)
nat_sgid = [nat_sg][0].id

mongodb_sg = create_security_group(vpc_con, group_name='mongodb', description='mongodb security group')
mongodb_sg_id = [mongodb_sg][0].id
sleep(1)

elasticsearch_sg = create_security_group(vpc_con, group_name='elasticsearch', description='elasticsearch security group')
elasticsearch_sg_id = [elasticsearch_sg][0].id
sleep(1)

tag_nat_sg = ResTags(resource_session).tag_securitygroup(False, nat_sgid, tags('nat security group for DBs'))
print tag_nat_sg

tag_mongodb_sg = ResTags(resource_session).tag_securitygroup(False, mongodb_sg_id, tags('DBs security group'))
print tag_mongodb_sg

tag_elasticsearch_sg = ResTags(resource_session).tag_securitygroup(False, elasticsearch_sg_id, tags('elasticsearch'))
print tag_elasticsearch_sg


def create_ingress_rules(resource_session, ipprotocol='tcp', sgid=nat_sgid, uidgp=[], from_port=80, to_port=80,
                         ipranges=[{'CidrIp': '0.0.0.0/0'}]):
    sg = resource_session.SecurityGroup(sgid)
    reponse = sg.authorize_ingress(IpPermissions=[
        { 'IpProtocol': ipprotocol,
          'FromPort': from_port,
          'ToPort': to_port,
          'IpRanges': ipranges,
          'UserIdGroupPairs': uidgp
          }])
    return reponse

# creating instances and setting up configurable items.
if results.image:
    default_image = results.image

if results.instance_type:
    default_inst_type = results.instance_type

if results.number_of_instances:
    maxcount = results.number_of_instances


def create_instance(subnet_id, inst_type, resource_session=resource_session, dryrun=False,
                    image_id=nat_image, maxcount=1, sshkey='ssh-key-pair-08-24-2014', instance_sg='default', public_ip=False):
    instance = resource_session.create_instances(DryRun=dryrun, ImageId=image_id, MinCount=1, UserData=fh.read(),
                                                 MaxCount=maxcount, KeyName=sshkey, InstanceType=inst_type,
                                                 NetworkInterfaces=[{'DeviceIndex': 0, 'SubnetId': subnet_id,
                                                                     'Groups': [instance_sg],
                                                                     'AssociatePublicIpAddress': public_ip}])
    return instance
nat_instance = create_instance(inst_type='m3.medium', subnet_id=get_sub_id_from_tag("public01"),
                               instance_sg=nat_sgid, public_ip=True)

nat_instance_id = nat_instance[0].id
waiter = client_session.get_waiter('instance_running')
waiter.wait(DryRun=False, InstanceIds=[nat_instance_id])


def get_network_ifc_id(resource_session=resource_session, nat_instance_id=nat_instance_id):
    instance = resource_session.Instance(nat_instance_id)
    all_attri = instance.network_interfaces_attribute
    for eni_id in all_attri:
        return eni_id['NetworkInterfaceId']

eni = get_network_ifc_id()
response = client_session.modify_network_interface_attribute(NetworkInterfaceId=eni,
                                                             SourceDestCheck={'Value': False})
print response

tag_nat_inst = ResTags(resource_session).tag_instance(False, nat_instance_id, tags('prod-nat-instance'))
print tag_nat_inst

squid_proxy = create_instance(image_id=squid_image, inst_type='m3.large',
                              subnet_id=get_sub_id_from_tag('private01'),
                              maxcount=1, instance_sg=default_sg, public_ip=False)

squid_proxy_id = squid_proxy[0].id
waiter.wait(DryRun=False, InstanceIds=[squid_proxy_id])

jump_host = create_instance(inst_type='m3.medium', subnet_id=get_sub_id_from_tag('public01'),
                            maxcount=1, instance_sg=default_sg, public_ip=True)
jump_host_id = jump_host[0].id
waiter.wait(DryRun=False, InstanceIds=[jump_host_id])

nat_table = create_routetable(vpc_id)
nat_table_id = [nat_table][0].id
sleep(1)

nat_tag_rt = ResTags(resource_session).tag_routetable(False, nat_table_id, tags('RouteTable with NatGateway'))
print nat_tag_rt

tag_squid_proxy = ResTags(resource_session).tag_routetable(False, squid_proxy_id, tags('squid-proxy'))
print tag_squid_proxy

tag_jump_host = ResTags(resource_session).tag_routetable(False, jump_host_id, tags('prod-jumphost'))
print tag_jump_host


def create_route(rt_id, nat_inst_id, cidrblock='0.0.0.0/0'):
    route = resource_session.RouteTable(rt_id)
    ig_route = route.create_route(DestinationCidrBlock=cidrblock, RouteTableId=nat_table_id, InstanceId=nat_inst_id)
    return ig_route

print create_route(nat_table_id, nat_instance_id)

for subnets in pri_only_subnets:
    print associate_with_subnet(nat_table_id, subnets)

#######################################################################################################################

def_vpc_con = resource_session.Vpc(default_vpc)
available_rts = list(def_vpc_con.route_tables.all())


def get_default_rt(tag, available_rts):
    for rt in available_rts:
        ftr = resource_session.RouteTable(rt.id)
        if ftr.tags[0].values() != []:
            if tag in ftr.tags[0].values():
                return ftr.id

def_rt_id = get_default_rt('default', available_rts)
backend_rt_id = get_default_rt('backend', available_rts)


def create_peering_route(rt_id=def_rt_id, vpc_p_id=None, cidrblock=None):
    route = resource_session.RouteTable(rt_id)
    ig_route = route.create_route(DestinationCidrBlock=cidrblock, VpcPeeringConnectionId=vpc_p_id)
    return ig_route

vpc_peering_connection = client_session.create_vpc_peering_connection(DryRun=False,
                                                                      VpcId=vpc_id,
                                                                      PeerVpcId=default_vpc,
                                                                      PeerOwnerId=userId)

vpc_peering_connection_id = vpc_peering_connection['VpcPeeringConnection']['VpcPeeringConnectionId']
vpc_peering = resource_session.VpcPeeringConnection(vpc_peering_connection_id)
vpc_peering.accept()

tag_pvc_peering = client_session.create_tags(DryRun=False, Resources=[vpc_peering_connection_id],
                                             Tags=tags(value=environment_name))

for subnets in all_vlans:
    print create_peering_route(cidrblock=subnets, vpc_p_id=vpc_peering_connection_id)

#for subnets in all_vlans:
#    print create_peering_route(rt_id=backend_rt_id, cidrblock=subnets, vpc_p_id=vpc_peering_connection_id)

for subnets in ['172.31.0.0/20', '172.31.16.0/20']:
    print create_peering_route(rt_id=nat_table_id, cidrblock=subnets, vpc_p_id=vpc_peering_connection_id)

#######################################################################################################################

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
