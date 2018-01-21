import re

# Open file get the file name and open it
fname = raw_input('Enter a file name: ')
if 1 > len(fname) :
    fname = 'mbox-short.txt'

try:
    fh=open(fname)
except:
    print 'Unble to open', fname
    exit()

rev_list = []

# Read each line and find out message count for each email address
for line in fh :
    rev = re.findall('^New Revision: (\d+)', line)
    if 1 > len(rev) :
        continue
    rev_list = rev_list + [int(rev[0])]
    print type(rev_list)

print 'Average Revision:', sum(rev_list)/len(rev_list)
