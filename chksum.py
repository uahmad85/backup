#!/usr/bin/python

import hashlib
import sys

file = sys.argv[1]
fhand = open(file)
data = fhand.read()
fhand.close()
checksum = hashlib.md5(data).hexdigest()
print checksum
