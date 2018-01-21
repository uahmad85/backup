import boto3

client = boto3.client("ec2")

client.authorize_security_group_ingress(GroupId = 'sg-267cfb41',
                                        IpPermissions=[ {'IpProtocol': 'tcp', 'FromPort': 8888, 'ToPort': 8888,
                                                         'UserIdGrupPairs': [{ 'GroupId':'sg-9e5bdff9'}]}])


def get_sg_from_tag(client_session, tag):
    security_groups = client_session.describe_security_groups()
    for group in security_groups['SecurityGroups']:
        if 'Tags' in group.keys():
            if 'close5-dev-security' in group['Tags'][0].values():
                return group['GroupId']