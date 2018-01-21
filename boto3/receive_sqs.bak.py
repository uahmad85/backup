#!/usr/bin/env python

from subprocess import check_call, CalledProcessError
import json

from peewee import *
import boto3

sqs = boto3.resource('sqs')
re_client = boto3.resource('ec2')
db = SqliteDatabase('InstInfo.db')
queue = sqs.get_queue_by_name(QueueName='InstanceTerminationNotice')
sqs_url = 'https://sqs.us-west-2.amazonaws.com/712818841314/InstanceTerminationNotice'


class InstInfo(Model):
    """Save instance id and fqdn for knife to remove nodes once they are scaled in"""
    id = CharField(max_length=255, unique=True)
    fqdn = CharField(max_length=255, unique=True)
    tags = TextField()

    class Meta:
        database = db


def initialize():
    """Create the database and the table if not exists"""
    db.connect()
    db.create_tables([InstInfo], safe=True)


def get_instance_info(instance_id):
    instance = re_client.Instance(instance_id)
    instance_info = {'id': instance.id, 'fqdn': instance.private_dns_name}
    if instance.tags:
        instance_info['tags'] = instance.tags
    else:
        instance_info['tags'] = 'No Tags'
    return instance_info

if __name__ == "__main__":
    initialize()
    while True:
        messages = queue.receive_messages(MaxNumberOfMessages=1, WaitTimeSeconds=1)
        if len(messages) == 0:
            break
        else:
            for message in messages:
                json_message = json.loads(message.body)
                _json = json.loads(json_message['Message'].encode('utf-8'))
                action = _json['Event']
                if action == "autoscaling:TEST_NOTIFICATION":
                    message.delete()
                    continue
                instance_id = _json['EC2InstanceId']
                instance = get_instance_info(instance_id)
                if action == 'autoscaling:EC2_INSTANCE_LAUNCH':
                    try:
                        InstInfo.create(id=instance['id'], fqdn=instance['fqdn'], tags=instance['tags'])
                        print "New Instance added ID: %s -- FQDN: %s" % (instance['id'], instance['fqdn'])
                        message.delete()
                    except IntegrityError as err:
                        print err
                        message.delete()
                else:
                    if action == 'autoscaling:EC2_INSTANCE_TERMINATE':
                        instance = InstInfo.get(id=instance_id)
                        del_node = "['knife', 'node', 'delete', '%s', '-y' ]" % instance.fqdn
                        del_client = "['knife', 'client', 'delete', '%s', '-y' ]" % instance.fqdn
                        print del_node
                        print del_client
                        #check_call(del_node)
                        #check_call(del_client)
                        InstInfo.delete().where(InstInfo.id == instance_id).execute()
                        message.delete()