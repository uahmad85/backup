ress = boto3.resource('ec2')
netw = ress.Instance('i-53582794')
netw.network_interfaces_attribute
netid = netw.network_interfaces_attribute
netid
for x in netid:
    print x
for x in netid:
    print x['NetworkInterfaceId']
ress = boto3.client('ec2')
ress.modify_network_interface_attribute(NetworkInterfaceId='eni-ee6b7e96', SourceDestCheck={ 'Value': False })

def get_network_ifc_id(resource_session, nat_instance_id):
    instance = resource_session.Instance(nat_instance_id)
    all_attri =instance.network_interfaces_attribute
    for eni_id in all_attri:
        return eni_id['NetworkInterfaceId']

