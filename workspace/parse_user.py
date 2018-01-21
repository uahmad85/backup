#!/usr/bin/python

import re
import os, sys, paramiko
paramiko.util.log_to_file('auto_ssh.log', 0)
from ConfigParser import SafeConfigParser
import threading
import Queue
import logging
import time
import getopt

logging.basicConfig(filename='threading.log', level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

threads = []
que_host = Queue.Queue()
hosts = []
cmd_list = []
file = '/Users/uahmad/python/paramiko/host_names'
fh = open(file)
 
parser = SafeConfigParser()
parser.read('.credentials')

def host_list(fh, hosts):
    if ',' in hosts:
        for host in hosts.split(','):
            que_host.put(host)
        return que_host
    else:
        if '*' in hosts:
            for host in fh:
                my_host = re.findall(hosts, host)
                if not my_host == []:
                    host_name = '%s' % my_host
                    que_host.put(host_name[2:-2])
        return que_host

def run_parallel(t, l, q):
    t = threading.Thread(name=host, target=t, args=(l, host))
    t.setDaemon(True)
    threads.append(t)
    t.start()
    logging.debug('Starting thread %s', t.getName())
    print threads

def print_out(channel, timeout=3.0):
    ''' print out stdout and stderr
    :param channel:
    :param timeout:
    '''
    while not channel.exit_status_ready():
        channel.settimeout(timeout)
        if channel.recv_ready():
            print channel.recv(2000),
        else:
            if channel.recv_stderr_ready():
                print channel.recv_stderr(2000),

def autoSsh(cmds, host, port=22, timeout=5.0, maxsize=2000):
    ''' run commands for given users, w/default host, port, and timeout, emitting to standard output all given commands and their responses 
(no more than 'maxsize' characters of each response).'''
    for section in parser.sections():
        cred = {key : val for key, val in parser.items(section)}
        try:
            transport = paramiko.Transport((host, port))
            transport.connect(**cred)
            channel = transport.open_session()
            if timeout: channel.settimeout(timeout)
            for cmd in cmd_list:
                channel.exec_command(cmd)
                print " "
                print 'hostname:%r -> Command:(%r)' % (host, cmd)
                print '-' * 85
                print_out(channel)
                time.sleep(1)
        except:
            err = sys.exc_info()
            print "ERR MSG: " + str(err[1]) 

if __name__== '__main__':
    logname = os.environ.get("LOGNAME", os.environ.get("USERNAME"))
    host = 'localhost' 
    port = 22
    usage = """ usage: %s [-h host] [-p port] [-f cmdfile] [-c "command"] user1 user2 ...\n -c command\n -f command file
 -h default host (default: localhost) \n -p default host (default: 22)
 Example: %s -c "echo $HOME" %s same as: \n %s -c "echo $HOME" -h %s@localhost:22 """ % (sys.argv[0], sys.argv[0], logname, sys.argv[0], logname)
    optlist, user_list = getopt.getopt(sys.argv[1:], 'c:f:h:p:l:', ['parallel'])
    if user_list:
        print usage
        sys.exit(1)
    for opt, optarg in optlist:
        if opt == '-f':
            for r in open(optarg, 'rU'):
                if r.rstrip():
                    cmd_list.append(r) 
        elif opt == '-c':
            command = optarg
            if command[0] == '"' and command[-1] == '"':
                command = command[1:-1]
            cmd_list.append(command)
        elif opt == '-h':
            host = optarg
            hosts = host_list(fh, host)
        elif opt == '-p':
            port = optarg
        elif opt == '--parallel':
            parallel = True
        else:
            print 'unknown option %r' % opt
            print usage
            sys.exit(1)

if parallel:
    answer = raw_input("plese confirm all the hosts that you want to execute the command on:\n%s (y): " % hosts.queue)
    if answer == 'y' or answer == 'Y':
        for host in range(len(hosts.queue)):
            host = hosts.get()
            run_parallel(autoSsh, cmd_list, host)      
    else:
        print "hostname(s) were not confirmed exiting!"
        sys.exit()

main_thread = threading.currentThread()
for t in threads:
    if t is not main_thread:
        logging.debug('Thread %s complete', t.getName())
        t.join()

if not parallel:
    if len(hosts.queue) > 1:
        answer = raw_input(" please confirm all the hosts that you want to execute the command on:\n%s (y): " % hosts.queue)
        if answer == 'y' or answer == 'Y':
            for host in range(len(hosts.queue)):
                host = hosts.get()
                autoSsh(cmd_list, host, port=port)
        else:
            print "hostname(s) were not confirmed exiting!"
            sys.exit()
    else:
        autoSsh(cmd_list, host, port=port)