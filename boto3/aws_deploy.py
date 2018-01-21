#!/usr/bin/env python
import re
import os, sys, paramiko
from ConfigParser import SafeConfigParser
import threading
import Queue
import logging
import time
import getopt
import boto3
import argparse

#command line arguments
parser = argparse.ArgumentParser(description='Usage: python aws_deploy.py [-H host] [-p port] [-f cmdfile] [-c "command"] user_name')
parser.add_argument('-u', '--user', action='store', default=False, help='user to run commands as i.e. ubuntu or ec2-user')
parser.add_argument('-H', '--host', action='store', default=False, help='hostname i.e. mongodb.example.com')
parser.add_argument('-f', '--host_file', action='store', default=False, help='file with server names')
parser.add_argument('-l', '--servers_list', action='store', default=False, help='list of servers to run commands on')
parser.add_argument('-c', '--command', action='store', default=False, help='commands to be executed')
parser.add_argument('-p', '--parallel', action='store_true', default=False, help="run commands on all the server in parallel")
parser.add_argument('-t', '--tag', action='store', default=False, help='AWS tag of component to run commands on')
results = parser.parse_args()

paramiko.util.log_to_file('/Users/sunahmad/old_data/python/paramiko/auto_ssh.log', 0)
logging.basicConfig(filename='/Users/sunahmad/old_data/python/paramiko/threading.log', level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

#vpc_id = 'vpc-d4f81ab1'
vpc_id = 'vpc-e76fbc83'
threads = []
que_host = Queue.Queue()
cmd_list = []
hosts = Queue.Queue()
#parallel = None
file = '/Users/sunahmad/old_data/python/paramiko/host_names'
fh = open(file)
optuser = None
cred = dict()
keypath = os.path.expanduser('~/.ssh/close5-lnp.pem')
#keypath = os.path.expanduser('~/.ssh/ssh-key-pair-08-24-2014.pem')
pkey = paramiko.RSAKey.from_private_key_file(keypath)
 
parser = SafeConfigParser()
parser.read('/Users/sunahmad/old_data/python/paramiko/.credentials')


def get_public_ip(vpcId, tag):
    ip_list = []
    client = boto3.resource('ec2')
    vpc = client.Vpc(vpcId)
    instances = vpc.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': [tag]}])
    for x in range(len(list(instances))):
        instance = client.Instance(list(instances)[x].id)
        ip_list.append(instance.public_ip_address)
    return ip_list


def host_list(fh, hosts):
    if ',' in hosts:
        for host in hosts.split(','):
            que_host.put(host)
        return que_host
    elif '*' in hosts:
        for host in fh:
            my_host = re.findall(hosts, host)
            if not my_host == []:
                host_name = '%s' % my_host
                que_host.put(host_name[2:-2])
    elif type(hosts) == list:
        for host in hosts:
            que_host.put(host)
        return que_host
    else:
        que_host.put(hosts)
    return que_host


def run_parallel(t, l, q):
    print t, l, q
    thread = threading.Thread(name=host, target=t, args=(l, q))
    thread.setDaemon(True)
    threads.append(thread)
    thread.start()
    logging.debug('Starting thread %s', thread.getName())


#def print_out(channel, timeout=3.0):
#    ''' print out stdout and stderr '''
#    while not channel.exit_status_ready():
#        channel.settimeout(timeout)
#        if channel.recv_ready():
#            print channel.recv(2000),
#        else:
#            if channel.recv_stderr_ready():
#                print channel.recv_stderr(2000),

def print_out(chan, timeout=3.0):
    while not chan.recv_exit_status():
        if chan.recv_ready():
            data = chan.recv(1024)
            while data:
                print data,
                data = chan.recv(1024)

        if chan.recv_stderr_ready():
            error_buff = chan.recv_stderr(1024)
            while error_buff:
                print error_buff,
                error_buff = chan.recv_stderr(1024)
        exist_status = chan.recv_exit_status()
        if 0 == exist_status:
            break

def autoSsh(cmds=None, host=None, port=22, timeout=5.0, maxsize=2000):
    ''' run commands for given users, w/default host, port, and timeout,
    emitting to standard output all given commands and their responses
(no more than 'maxsize' characters of each response).'''
    for section in parser.sections():
        for key, val in parser.items(section):
            if optuser:
                cred['username'] = optuser
                cred['pkey'] = pkey
            else:
                cred['username'] = 'ubuntu'
                cred['pkey'] = pkey
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

if results.host_file:
    print "got here"
    for r in open(results.host_file, 'rU'):
        host = r.strip('\n')
        hosts.put(host)

if results.command:
    if results.command[0] == '"' and results.command[-1] == '"':
        command = results.command[1:-1]
    cmd_list.append(results.command)

if results.host:
    hosts = host_list(fh, results.host)

if results.tag:
    hosts = host_list(fh, get_public_ip(vpc_id, results.tag))

if results.user:
    optuser = results.user

if results.parallel:
    answer = raw_input("plese confirm all the hosts that you want to execute the command on:\n%s? (y/n [y]): " % hosts.queue)
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
        sys.exit()

if not results.parallel and len(hosts.queue) >= 1:
    answer = raw_input(" please confirm all the hosts that you want to execute the command on:\n%s? (y/n [y]): " % hosts.queue)
    if answer == 'y' or answer == 'Y':
        for host in range(len(hosts.queue)):
            host = hosts.get()
            autoSsh(cmd_list, host)
    else:
        print "hostname(s) were not confirmed exiting!"
        sys.exit()
else:
    print "Tag or Regex does not match any instance: %s" % results.tag
    sys.exit()
