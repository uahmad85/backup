import boto3
import sys

from tag_resources import ResTags

session = boto3.resource('ec2')
client_session = boto3.client('ec2')
resource_session = boto3.resource('ec2')


all_vpcs = client_session.describe_vpcs()
subnet_tag = "public"
instance_tag = Tags=[
    {
        'Key': 'Name',a
       'Value': 'core-api'},]


# get vpc id
def get_vpc_id(vpcs, vpc_tag):
    for vpc in vpcs['Vpcs']:
        if 'Tags' in vpc.keys():
            for tag in vpc['Tags']:
                if vpc_tag in tag.values():
                    vpc_id = vpc['VpcId']
                    return vpc_id

vpc_id = get_vpc_id(all_vpcs, 'close5-dev')
#print "from vpcs", vpc_id

# get all subnet for a vpc from vpc_id
vpc_conn = resource_session.Vpc(vpc_id)


def get_all_vpc_sub(vpc_conn):
    subnet_list = []
    subnets = list(vpc_conn.subnets.all())
    for sub in subnets:
        subnet = str(sub).split('=')[1].strip()[1:-2]
        subnet_list.append(subnet)
    return subnet_list
available_subnet = get_all_vpc_sub(vpc_conn)
print available_subnet

def sub_for_instances(client_session, sub_list, tag):
    subnet = client_session.describe_subnets(DryRun=False,
                                             SubnetIds=sub_list,
                                             Filters=[ { "Name": "tag:Name",
                                                         "Values": [ tag ] }, ])
    for sub in subnet['Subnets']:
        return sub['SubnetId']

sub_for_instances(client_session, available_subnet, subnet_tag)

vpc-e76fbc83
AMI ID
node-0.12.13 (ami-0bc0316b)
Subnet ID
subnet-30f0f969

def mk_inst(session,
           dryrun=False,
           image_id='ami-0bc0316b',
           maxcount=10,
           sshkey='close5-dev',
           subnet_id='',
           inst_type='t2.micro'
           ):
    instance = session.create_instances(
        DryRun=dryrun,
        ImageId=image_id,
        MinCount=1,
        MaxCount=maxcount,
        KeyName=sshkey,
        SubnetId=subnet_id,
        InstanceType=inst_type)
    return instance


instance = mk_inst(resource_session)
instance_id = instance[0].id
tag_inst = ResTags(resource_session).tag_instance(False, instance_id, instance_tag)
