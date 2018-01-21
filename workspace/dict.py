#!/usr/bin/python

lst = ['zhen','marquard','cwen','csev','zhen','zhen','cdev','marquard','marquard','csev','cwen','zhen','zhen','sunny', 'sunny']
count = dict()
for name in lst:
    count[name] = count.get(name,0) + 1
    
newdict = count
print list(count)
for key in newdict:
       print key, count[key]
