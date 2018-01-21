#!/usr/bin/env python

import boto3

resource_session = boto3.resource('ec2')


class ResTags():
    resource_session = resource_session

    def __init__(self, resource_session):
        self.resource_session = resource_session

    def tag_instance(self, dryrun, id, tag):
        instance = self.resource_session.Instance(id)
        Tags = instance.create_tags(DryRun=dryrun, Tags=tag)
        return Tags

    def tag_vpc(self, dryrun, id, tag):
        instance = self.resource_session.Vpc(id)
        Tags = instance.create_tags(DryRun=dryrun, Tags=tag)
        return Tags

    def tag_subnet(self, dryrun, id, tag):
        instance = self.resource_session.Subnet(id)
        Tags = instance.create_tags(DryRun=dryrun, Tags=tag)
        return Tags

    def tag_internetgateway(self, dryrun, id, tag):
        instance = self.resource_session.InternetGateway(id)
        Tags = instance.create_tags(DryRun=dryrun, Tags=tag)
        return Tags

    def tag_routetable(self, dryrun, id, tag):
        instance = self.resource_session.RouteTable(id)
        Tags = instance.create_tags(DryRun=dryrun, Tags=tag)
        return Tags

    def tag_securitygroup(self, dryrun, id, tag):
        instance = self.resource_session.SecurityGroup(id)
        Tags = instance.create_tags(DryRun=dryrun, Tags=tag)
        return Tags