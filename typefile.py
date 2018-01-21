#!/usr/bin/python
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-F', type=file)
parser.add_argument('-o', metavar='out-file', type=argparse.FileType('wt'))

try:
    results = parser.parse_args()
    print 'Input file:', results.F
    print 'Output file:', results.o
except IOError, msg:
    parser.error(str(msg))
for x in results.F:
    print x
