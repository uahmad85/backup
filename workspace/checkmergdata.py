#!/usr/bin/python
from subprocess import Popen, PIPE
file = raw_input(':>' )
if len(file) == 0 : file = 'mfiles'
fh = open(file)

for f in fh:
    f = f.split()[0]
    proc = Popen('cat %s' % (f), stdout=PIPE, shell=True)
    out = Popen(['grep ', ' mobi*'], stdin=proc.stdout, stdout=PIPE, shell=True).communicate()[0]
    proc.stdout.close()
    out
