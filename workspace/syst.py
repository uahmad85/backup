import sys

print 'tatal args:', len(sys.argv)
print 'sys.args[1]', sys.argv[1]
print 'sys.args[2:]', sys.argv[2:]
if len(sys.argv) < 3:
    print "need at least two agrs zip_file and arc_file!"
    sys.exit()
else:
    for file in sys.argv[2:]:
        arc_file = file
        print arc_file, type(arc_file)
