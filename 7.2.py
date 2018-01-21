#!/usr/bin/python

count = 0
tot_spam = 0
lst = list()
file = raw_input('Enter file name: ')
if len(file) == 0 : file = 'mbox-short.txt'
try:
    fh = open(file)
except IOError as io:
    print io
    exit()
for line in fh:
    line = line.rstrip()
    if not line.startswith('X-DSPAM-Confidence:') : continue
    #lst.append(float(line.split()[1]))
    total_spam = float(line.split()[1])
    count = count + 1
    tot_spam = tot_spam + total_spam
    avg_spam = tot_spam / count
print 'Average spam confidence:', repr(avg_spam).rjust(3)
