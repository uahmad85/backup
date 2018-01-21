#!/usr/bin/python

import argparse
import os

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-F', action='store', dest='file', help='File name')
result = parser.parse_args()
print result
try:
    filename = result.file.split(',')
except AttributeError as error:
    print error
print filename
for x in filename:
    if os.path.isfile(x):
        size = os.path.getsize(x)
        print 'File: {0}, Size: {1}, Status: exists'.format(x, size)
    else:
        print 'file %s does not exist' % (x)
