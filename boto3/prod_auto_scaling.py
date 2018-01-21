#!/usr/bin/env python
import boto3
from autoscaling import AutoScalingGroup
from time import sleep

client = boto3.client('autoscaling')
auto_scaling = AutoScalingGroup('session')
auto_scaling.default_tags = 'core-api'
auto_scaling.default_image_id = 'ami-c9887ba9'
auto_scaling.default_instance_type = 'm4.large'

des_la_cfg = client.describe_launch_configurations()
if not des_la_cfg['LaunchConfigurations']:
    lunch_config = auto_scaling.create_launch_config()
elif des_la_cfg['LaunchConfigurations'][0]['LaunchConfigurationName'] != "core-api":
    lunch_config = auto_scaling.create_launch_config()
    print lunch_config

scaling_group = auto_scaling.create_auto_scaling()
print scaling_group

scaling_up_policy = auto_scaling.put_scaling_policy(scaling_adjustment=1)
print scaling_up_policy

scaling_down_policy = auto_scaling.put_scaling_policy(scaling_adjustment=-1, policy_name='scaling down')
print scaling_down_policy

scale_up_metric_alarm = auto_scaling.put_metric_alarm(es_name='core-api', alarm_name="scaling up",
                                                      alarm_actions=[scaling_up_policy['PolicyARN']])
print scale_up_metric_alarm

scale_down_metric_alarm = auto_scaling.put_metric_alarm(es_name='core-api', alarm_name="scaling down",
                                                        alarm_description='scaling down polity',
                                                        alarm_actions=[scaling_down_policy['PolicyARN']],
                                                        comparison_operator='LessThanOrEqualToThreshold', threshold=30)
print scale_down_metric_alarm

sleep(3)
######   cunsumer-server setup   ##########
sleep(3)

auto_scaling.default_tags = 'images-server'

scaling_group = auto_scaling.create_auto_scaling(min=3, max=10)
print scaling_group

images_scaling_up_policy = auto_scaling.put_scaling_policy(scaling_adjustment=1, policy_name='images scaling up')
print images_scaling_up_policy

images_scaling_down_policy = auto_scaling.put_scaling_policy(scaling_adjustment=-1, policy_name='images scaling down')
print images_scaling_down_policy

images_scale_up_metric_alarm = auto_scaling.put_metric_alarm(es_name='images-server', alarm_name="images scaling up",
                                                             alarm_actions=[images_scaling_up_policy['PolicyARN']])
print images_scale_up_metric_alarm

images_scale_down_metric_alarm = auto_scaling.put_metric_alarm(es_name='images-server', alarm_name="images scaling down",
                                                               alarm_description='scaling down polity',
                                                               alarm_actions=[images_scaling_down_policy['PolicyARN']],
                                                               comparison_operator='LessThanOrEqualToThreshold',
                                                               threshold=30)
print images_scale_down_metric_alarm
