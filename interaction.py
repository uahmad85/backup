import subprocess

print 'One line at a time:'
proc = subprocess.Popen('python repeater.py', 
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        )
for i in range(10):
    proc.stdin.write('%d\n' % i)
    output = proc.stdout.readline()
    print output.rstrip()
remainder = proc.communicate()[0]
print remainder

print
print 'All output at once:'
proc = subprocess.Popen('python repeater.py', 
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        )
for i in range(10):
    proc.stdin.write('%d\n' % i)

output = proc.communicate()[0]
print output
