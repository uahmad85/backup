cont = 0
fle = 'counter'
fh = open(fle, 'w')
fhr = open(fle, 'r')
numer = 1
import sys
import time
def follow(thefile):
    thefile.seek(0,2) # Go to the end of the file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1) # Sleep briefly
            continue
        yield linie

for x in range(100):
    fh.write(str(x) + '\n')
    print len(follow(fhr))
fh.close()
a = [i for i in fhr.read().split('\n') if i][-1]
print a