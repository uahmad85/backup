from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('credentials')

for sec in parser.sections():
        print '%-12s: %s' % (sec, parser.has_section(sec))
        