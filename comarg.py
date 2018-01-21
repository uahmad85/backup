#!/usr/bin/python

import sys

name = sys.argv[1]
handle = open(name, 'r')
text = handle.read()

#print 'count:', len(sys.argv)
#print 'type:', type(sys.argv)
#for arg in sys.argv:
print name, 'is', len(text), 'bytes'
