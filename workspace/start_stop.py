#!/usr/bin/python
from time import sleep
from subprocess import Popen, PIPE, call

ssh_user = "ubuntu"
db_host = '172.31.14.195'
ssh_key = "/home/ubuntu/.ssh/es-test.pem"
start_mongodb = "sudo service mongod start"
status_mongodb = "sudo service mongod status"
stop_mongodb = "sudo service mongod stop"

command = 'ssh -o StrictHostKeyChecking=no -i %s %s@%s %s' % (ssh_key,
                                                              ssh_user,
                                                              db_host,
                                                              status_mongodb)

status = call(command, shell=True)
try:
    if status != 0:
        print "mongodb is already stoped!"
    else:
        print 'stopping mongodb...'
        proc = Popen('ssh -o StrictHostKeyChecking=no -i %s %s@%s %s' % (ssh_key,
                                                                         ssh_user,
                                                                         db_host,
                                                                         stop_mongodb), stdout=PIPE, shell=True).communicate()[0]
        proc
except:
    err = sys.exc_info()
    print "ERR MSG: " + str(err[1])

#start mongodb
sleep(5)
proc = Popen('ssh -o StrictHostKeyChecking=no -i %s %s@%s %s' % (ssh_key,
                                                                 ssh_user,
                                                                 db_host,
                                                                 start_mongodb), shell=True).communicate()[0]
proc