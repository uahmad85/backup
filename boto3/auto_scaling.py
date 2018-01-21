#!/usr/bin/env python
import boto3

session = boto3.resource('ec2')
client_session = boto3.client('ec2')
resource_session = boto3.resource('ec2')
config_client_session = boto3.client('autoscaling')
client = boto3.client('cloudwatch')

user_data_file = '/Users/sunahmad/bootstrap.sh'
fh = open(user_data_file)
instance_tag = Tags=[
    {
        'Key': 'Name',
        'Value': 'core-api'}]


def create_auto_scaling(as_name=None, config_name=None, elb_name='core-api', min=5, max=10):
    response = config_client_session.create_auto_scaling_group(
        AutoScalingGroupName=as_name,
        LaunchConfigurationName=config_name,
        MinSize=min, MaxSize=max,
        DesiredCapacity=min,
        HealthCheckGracePeriod=30,
        VPCZoneIdentifier='subnet-30f0f969, subnet-0d855f69',
        LoadBalancerNames=[ elb_name ],
        HealthCheckType='ELB', DefaultCooldown=10,
        Tags=[{ 'Key': 'Name', 'Value': 'core-api', 'PropagateAtLaunch': True}]
        )
    return response

auto_scaling_group = create_auto_scaling(as_name='testrun', config_name='testrun')
print auto_scaling_group


def put_scaling_policy(as_name=None, scaling_adjustment=None, pc_name="scaling up"):
    response = config_client_session.put_scaling_policy(
        AutoScalingGroupName=as_name,
        PolicyName=pc_name,
        PolicyType='SimpleScaling',
        AdjustmentType='ChangeInCapacity',
        ScalingAdjustment=scaling_adjustment,
        Cooldown=300)
    return response

scaling_up_policy = put_scaling_policy('testrun', 1)
scaling_down_policy = put_scaling_policy('testrun', -1, pc_name='scaling down')
print scaling_up_policy
print scaling_down_policy


def put_metric_alarm(alarm_name=None, alarm_description= "scaling up policy", alarm_actions=None,
                     metric_name='CPUUtilization', comparison_operator='GreaterThanOrEqualToThreshold', threshold=70 ):
    response = client.put_metric_alarm(
        AlarmName=alarm_name,
        AlarmDescription=alarm_description,
        ActionsEnabled=True,
        AlarmActions=alarm_actions,
        Namespace='AWS/EC2',
        Statistic='Average',
        Dimensions=[
            {
                'Name': 'AutoScalingGroupName',
                'Value': 'testrun'
            },
        ],
        MetricName=metric_name,
        ComparisonOperator=comparison_operator,
        Threshold=threshold,
        Unit='Seconds',
        Period=180,
        EvaluationPeriods=2)
    return response

print put_metric_alarm(alarm_name="scaling up", alarm_actions=[scaling_up_policy['PolicyARN']])
print put_metric_alarm(alarm_name="scaling down", alarm_description='scaling down polity', alarm_actions=[scaling_down_policy['PolicyARN']],
                       comparison_operator='LessThanOrEqualToThreshold', threshold=30)