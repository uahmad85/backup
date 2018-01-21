#!/usr/bin/python
import re

#file = raw_input(':> ')
#if len(file) =
file = '/Users/uahmad/python/mbox-short.txt'
fh = open(file)

for word in fh:
    word = word.rstrip()
    re.search(r'Received: from (\S+\.\S+\.\S+?)', word)
    print word
#mat = email.next()
#print mat.groups()

    #pat = re.compile(r'Received: from (?p<emails>\S+\.\S+\.\S+)')
    #all_email = pat.findall(word).groupdict()
    #email = re.compile(r"Received: from (\S+\.\S+\.\S+)")
    #all_email = email.finditer(word)
    #mat = all_email.next()
    #mat.groups
    #pat = re.compile(r'Re
    
    
