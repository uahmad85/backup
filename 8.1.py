#!/usr/bin/python
lst =  []

file = raw_input('file name please: ')
if len(file) == 0 : file = 'romeo.txt'
try:
    fh = open(file)
except IOError as io:
    print io, 'please enter the file name again'
    exit()
data = fh.read()
words = data.split()
for word in words:
    if not word in lst:
        lst.append(word)
lst.sort()
print lst
