#!/usr/bin/env python
import json

from peewee import *
import boto3

sqs = boto3.client('sqs')
sqs_url = 'https://sqs.us-west-2.amazonaws.com/712818841314/InstanceTerminationNotice'
db = SqliteDatabase('InstInfo.db')


class InstInfo(Model):
    """Save instance id and fqdn for knife to remove nodes once they are scaled in"""
    content = TextField()

    class Meta:
        database = db


def initialize():
    """Create the database and the table if not exists"""
    db.connect()
    db.create_tables([InstInfo], safe=True)
