#!/usr/bin/python

import re
fh =open('mbox-short.txt')
for line in fh:
    line = line.rstrip()
    if re.search('From:', line):
        print line
