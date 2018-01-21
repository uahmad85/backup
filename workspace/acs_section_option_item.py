from ConfigParser import SafeConfigParser
import os
parser = SafeConfigParser()
parser.read('credential')

dic = dict()
for sec in parser.sections():
    print 'Sections:', sec
    print 'Options:', parser.options(sec)
    for key, val in parser.items(sec):
        dic[key] = val
    print dic, os.path.isfile()