from ConfigParser import SafeConfigParser

hosts = []
cmd_list = []

parser = SafeConfigParser()
my_cred = parser.read('.credentials')
print my_cred
for section in parser.sections():
    cred = {key : val for key, val in parser.items(section)}
    print cred
