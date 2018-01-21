#!/usr/bin/python
smallest = None
total = 0
count = 0
lst = [9, 41, 12, 3, 74, 15]

for num in lst:
    if smallest is None:
        smallest = num
    if num < smallest:
        smallest = num
    total = total + num

print 'After', smallest, total
