#!/usr/bin/python

import os
from subprocess import call

dir_name = raw_input('path name: ')
lst = list()
x = 1
cmd = call(['touch', str(x)])
hme = '/Users/uahmad/python'
if os.path.isdir(dir_name):
    print ''
    print 'searching for the directory....... ', dir_name
else:
    print 'directory doesnt exist: ', dir_name
    exit()
for dir, dirname, file in os.walk(dir_name):
    if len(dirname) == 0:
        continue
    else:
        print dirname
        for d in dirname:
            os.chdir(d)
            call(['touch', str(x)+'.txt'])
            os.chdir(hme)
            x += 1
            for d, dr, f in os.walk(dir_name):
               if len(f) == 0:
                   continue
               else:
                   print f
                   for i in f:
                       if i.endswith('.txt'):
                           print(os.path.join(dr, i))
a = "one"
raw