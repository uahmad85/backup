#!/usr/bin/python

file = raw_input('Enter file name: ')
if len(file) == 0 : file = 'words.txt'
try:
    fh = open(file)
except IOError as io:
    print io
    exit()
for words in fh:
    print words.rstrip().upper()
