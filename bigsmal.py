#!/usr/bin/python
exist = False
lst = []
largest = 1
smallest = 1000
while True:
    num = raw_input("Enter a number: ")
    if num == "done": 
        break
    lst.append(num)
    intlst = [int(x) for x in lst]
    for x in intlst:
        if x > largest:
            largest = x
        if x < smallest:
            smallest = x
        if 21 in intlst:
            exist = True
print "Maximum", largest
print "Smallest", smallest
print lst
print '21 in the list',exist
