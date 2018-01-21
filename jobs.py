#!/usr/bin/python

import requests
import json
headers = {'content-type': 'application/json'}
data = {
    'first_name': 'sunny ahmad',
    'last_name': 'Ahmad',
    'email': 'uahmad85@gmail.com',
    'phone': '9195939243',
    'cover_letter': 'I am interested in the DevOps / Engineer role with your organization.'
                    'I find this to be a very interesting opportunity'
                    ' and I have been looking for an organization where I can better utilize'
                    ' my experience and skillset to make a major contribution.'
                    ' I have 8+ years of experience working with Linux, AWS (Certified),'
                    ' VMware Virtualization systems. I have Very good knowledge/experience with Puppet (Certified),'
                    ' and I am also a Red Hat Certified Systems Administrator (RHCSA #130-016-298).',
    'urls': ['https://www.linkedin.com/in/usman-ahmad-4a329970/']
}

post = requests.post('https://app.close.io/hackwithus/', data=json.dumps(data), headers=headers)
print(post.status_code, post.reason, post.text)
