#!/usr/bin/env python

import json


def tags(key='Name', value=None):
    Tags=[
        {'Key': key,
         'Value': value}
    ]
    return "Tags=%s" % Tags


print tags(value='core-api')