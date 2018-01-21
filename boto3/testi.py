import boto3

def lc_exists():
    client = boto3.client('autoscaling')
    lc = client.describe_launch_configurations()
    if len(lc) > 0:
        for x in range(len(lc['LaunchConfigurations'])):
            print lc['LaunchConfigurations'][x]['LaunchConfigurationName']
            if lc['LaunchConfigurations'][x]['LaunchConfigurationName'] == 'staging-api':
                print "yes %s" % lc['LaunchConfigurations'][x]['LaunchConfigurationName']

lc_exists()
