def create_launch_config(self, config_name, instancetype, image_id):
    launch_config = self.autoscaling_client_session.create_launch_configuration(LaunchConfigurationName=config_name,
                                                                                ImageId=image_id, KeyName='close5-lnp',
                                                                                SecurityGroups=['default'],
                                                                                InstanceType=self.default_instance_type, UserData=fh.read(),
                                                                                IamInstanceProfile='read_only_access_for_ec2',
                                                                                AssociatePublicIpAddress=True)
return launch_config









print create_launch_config('testrun', 't2.micro', 'ami-0bc0316b')


elb = create_elb('testrun', ['subnet-30f0f969', 'subnet-0d855f69'], 'core-api')
elb_dns_name = elb['DNSName']



def put_metric_alarm(name):
    response = client.put_metric_alarm(
        AlarmName=name,
        AlarmDescription='scale up policy',
        ActionsEnabled=True,
        AlarmActions=[scaling_up_policy['PolicyARN']],
        Namespace='AWS/EC2',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'AutoScalingGroupName',
                'Value': 'testrun'
            },
        ],
        MetricName='CPUUtilization',
        ComparisonOperator='GreaterThanOrEqualToThreshold',
        Threshold=70,
        Unit='Seconds',
        Period=60,
        EvaluationPeriods=2)
    return response

    #print put_metric_alarm('scalup')

#response = config_client_session.delete_auto_scaling_group(
#    AutoScalingGroupName='testrun-consumer',
#    ForceDelete=True
#)
