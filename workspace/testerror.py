import os, errno

try:
    f = open('asdfasdf', 'r')
except IOError, ioex:
    print 'errno:', ioex.errno
    print 'err code:', errno.errorcode[ioex.errno]
    print 'err message:', os.strerror(ioex.errno)
