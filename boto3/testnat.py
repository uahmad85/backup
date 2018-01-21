import boto3

resource_session = boto3.resource('ec2')
client_session = boto3.client('ec2')

nat_sgid = 'sg-13fe5674'


def get_sub_id_from_tag(sub_tag, client_session=client_session):
    alls = client_session.describe_subnets()
    for sub in alls['Subnets']:
        if 'Tags' in sub.keys():
            if sub_tag in sub['Tags'][0].values():
                return sub['SubnetId']


def create_instance(subnet_id, resource_session=resource_session, dryrun=False, image_id='ami-9abea4fb', maxcount=1,
                    sshkey='close5-dev', inst_type='t1.micro', instance_sg='default', public_ip=False):
    instance = resource_session.create_instances(DryRun=dryrun, ImageId=image_id, MinCount=1,
                                                 MaxCount=maxcount, KeyName=sshkey, InstanceType=inst_type,
                                                 NetworkInterfaces=[{'DeviceIndex': 0, 'SubnetId': subnet_id,
                                                                     'Groups': [instance_sg],
                                                                     'AssociatePublicIpAddress': public_ip}])
    return instance

nat_instance = create_instance(image_id='ami-030f4133', subnet_id='subnet-ce46b3aa', instance_sg=nat_sgid, public_ip=True)

nat_instance_id = nat_instance[0].id
print nat_instance_id
