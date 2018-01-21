#!/usr/bin/env python

import boto3
import os

resource_session = boto3.resource('ec2')
vpc_con = resource_session.Vpc('vpc-e76fbc83')


def check_security_group(vpc, tag=None):
    for i in vpc.security_groups.filter(Filters=[{"Name":"group-name", "Values": [tag]}]):
        if i == "":
            return False
        else:
            print "security group already exists: {0}".format(resource_session.SecurityGroup([i][0].id).tags)
            return True

#resource_session.SecurityGroup([i][0].id).tags

print check_security_group(vpc_con, tag='vpc_nat')
