#!/usr/bin/env python
import boto3
import os

client = boto3.client('elasticbeanstalk')
ebEnvs = client.describe_environments()
ebEnvsList = ebEnvs['Environments']
AppNamesList = []

for env in ebEnvsList:
    AppNamesList.append(env['ApplicationName'])
setList = set(AppNamesList)
print len(setList)

for app in setList:
    print "########%s" % (len(app) * '#' + '##')
    print "##   %s   ##" % app
    print "########%s" % (len(app) * '#' + '##')
    ebEnvsByApp = client.describe_environments(ApplicationName=app)
    perSiteEnvs = ebEnvsByApp['Environments']
    for env in perSiteEnvs:
        print "%s" % env['EnvironmentName']
    print ""
