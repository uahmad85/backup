#!/usr/bin/python
import re

def compavg():
    value = []
    file = raw_input('Enter file:')
    if len(file) == 0 : file = 'mbox-short.txt'
    try:
        fhand = open(file, 'r')
    except:
        print "file name doesn't exist!"
        exit()

    for val in fhand:
        val = val.rstrip()
        num = re.findall('^New Revision: (\d+)', val)
        if len(num) == 0:
            continue
        value.extend(num)
        value = [float(i) for i in num]
        average = sum(value) / len(value)
    print average


compavg()
