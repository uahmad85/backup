import ConfigParser

parser = ConfigParser.SafeConfigParser()
parser.read('credentials')

parser.add_section('bug_tracker_new')
parser.set('bug_tracker_new', 'url', 'http://localhost:8080/bugs')
parser.set('bug_tracker_new', 'username', 'dhellmann')
parser.set('bug_tracker_new', 'password', 'secret')

for section in parser.sections():
    cred = {key : val for key, val in parser.items(section)}
    print cred   
      #for name, value in parser.items(section):
    #   print '  %s = %r' % (name, value)
    