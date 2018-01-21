#!/usr/bin/python

file = raw_input('> ')
if len(file) == 0 : file = 'romeo.txt'
fh = open(file)
dic = {}
lst = []
#data = fh.read().split()
#print data
for line in fh:
    words = line.split()
    for word in words:
        dic[word] = dic.get(word,0) + 1

for key, val in dic.items():
    lst.append( (val, key) )
    
lst.sort(reverse=True)

for val, key in lst[:10]:
    print key, val
