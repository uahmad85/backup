import boto3

def lc_lists():
    lc_list = []
    client = boto3.client('autoscaling')
    lc = client.describe_launch_configurations()
    if len(lc) > 0:
        for x in range(len(lc['LaunchConfigurations'])):
            lc_list.append(lc['LaunchConfigurations'][x]['LaunchConfigurationName'])
    return lc_list

def lc_exists(tag, lc_list):
    if tag in lc_list:
        print "lc is already in lc_list: %s " % lc_list
        return True
    else:
        print "lc does not exists: %s " % tag
        return False

print lc_exists('staging-api', lc_lists())
