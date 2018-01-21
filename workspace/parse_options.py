from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('credentials')

for sec in parser.sections():
    for opt in parser.options(sec):
        print '%s.%-12s : %s' % (sec, opt, parser.has_option(sec, opt))
        