#!/usr/bin/env python

import boto3
import redis
import argparse
import random


parser = argparse.ArgumentParser(description='Usage: redis_failover.py -i <rep_group_id> -r <region>')
parser.add_argument('-i', '--rep_group_id', action='store', help='replication group id of the cluster')
parser.add_argument('-b', '--eb_id', action='store', help='beanstalk instance id for consumer that is using redis')
parser.add_argument('-r', '--region', action='store', help='region of cache cluster, Default region is set in your ~/HOME/.aws/config')
results = parser.parse_args()

# settings up region.
cur_region = 'us-west-2'
rep_group_id = 'testing'

if results.region:
    cur_region = results.region

if results.rep_group_id:
    rep_group_id = results.rep_group_id

# get info on replication group.
client = boto3.client('elasticache', region_name=cur_region)
eb_client = boto3.client('elasticbeanstalk', region_name=cur_region)
response = client.describe_replication_groups(ReplicationGroupId=rep_group_id)

# cluster's members.
mem_clusters = response['ReplicationGroups'][0]['MemberClusters']
print "all nodes: {0}".format(mem_clusters)


def get_endpoint(role):
    dic = {}
    for node in response['ReplicationGroups'][0]['NodeGroups']:
        for i in range(len(node['NodeGroupMembers'])):
            if node['NodeGroupMembers'][i]['CurrentRole'] == role:
                dic['redis_host'] = node['NodeGroupMembers'][i]['ReadEndpoint']['Address']
                dic['cluster_id'] = node['NodeGroupMembers'][i]['CacheClusterId']
                return dic

primary_host = get_endpoint('primary')
print "primary node: {0}".format(primary_host)

mem_clusters.remove(primary_host['cluster_id'])
print "replica node(s): {0}".format(mem_clusters)

r = redis.StrictRedis(host=primary_host['redis_host'], port=6379)
#print r.get('foo')

cluster_node = client.describe_cache_clusters(CacheClusterId=primary_host['cluster_id'])
if cluster_node['CacheClusters'][0]['CacheClusterStatus'] != 'available':
    rreplica = random.choice(mem_clusters)
    waiter = client.get_waiter('cache_cluster_available')
    waiter.wait(CacheClusterId=primary_host['cluster_id'])
    waiter = client.get_waiter('replication_group_available')
    waiter.wait(ReplicationGroupId=rep_group_id)
    pormote_rreplica = client.modify_replication_group(ReplicationGroupId=rep_group_id, PrimaryClusterId=rreplica, ApplyImmediately=True)
    waiter = client.get_waiter('cache_cluster_available')
    waiter.wait(CacheClusterId=rreplica)
    print "PendingModifiedValues: {0}".format(pormote_rreplica['ReplicationGroup']['PendingModifiedValues'])
    # restart the app once redis primary has changed.
    if results.eb_id:
        eb_client.restart_app_server(EnvironmentId=results.eb_id)