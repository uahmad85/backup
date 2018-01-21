#!/usr/bin/python
lst =  []
count = 0
file = raw_input('file name please: ')
if len(file) == 0 : file = 'mbox-short.txt'
try:
    fh = open(file)
except IOError as io:
    print io, 'please enter the file name again'
    exit()
for line in fh:
    line = line.rstrip()
    if line.startswith('From '):
       count = count + 1
       email = line.split()[1]
       print email
print 'There were {} lines in the file with From as the first word'.format(count)
