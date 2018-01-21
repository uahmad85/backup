#!/usr/bin/python
lst =  []
count = dict()
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
       line = line.split()[1]
       count[line] = count.get(line, 0) + 1
frequent = max(count.values)
print frequent
