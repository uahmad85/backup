#!/usr/bin/python
from ConfigParser import SafeConfigParser
import glob

parser = SafeConfigParser()

files = ['1', '2',
         'media', 'upload']
found = parser.read(files)

missing = set(files) - set(found)
print 'found files:', found
print 'missing:', missing