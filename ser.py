
import re
hand = open('/Users/uahmad/python/mbox-short.txt') 
for line in hand:
    line = line.rstrip()
    if re.search('From:', line) :
        print line