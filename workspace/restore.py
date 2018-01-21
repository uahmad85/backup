#!/usr/bin/python
import os
from subprocess import Popen, PIPE
from time import sleep
import sys
import MySQLdb
import _mysql
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('.credentials')

credentials = dict()
for sec in parser.sections():
    for key, val in parser.items(sec):
        credentials[key] = val
    #print credentials


# grab the directory and db list.
dir_path = raw_input('Enter the backup directory name where you have dump files: ')
if len(dir_path) == 0 : dir_path = '/home/devops/mobitv'
files = os.listdir(dir_path)
print ''
print '#' * 60
print 'Populaing a list of all the Databases that will be restored.'
print '#' * 60
sleep(1)
print ''
lst = list()
def get_db():
    for file in files:
        db = file.split('-')[0]
        lst.append(db)
    return lst

for db in get_db():
    print db
print ''
print '#' * 60
sleep(2)
for db in files:
    db = db.split('-')[0]
    db_con = _mysql.connect(**credentials)
    db_con.query('select version();')
    result = db_con.store_result()
print 'MySQL Verion:', result.fetch_row(0)
print '#' * 60

# geting the absolute path for dump files.
for file in files:
    rest_file = os.path.join(dir_path + '/' + file)
    db = rest_file.split('/')[4].split('-')[0]
    process_db = Popen('mysql -u%s -p%s -S%s' % (credentials['user'], credentials['passwd'], credentials['unix_socket']), stdout=PIPE, stdin=PIPE, shell=True)
    out_db = process_db.communicate('create database if not exists ' + db)
    out_db
    process1 = Popen('mysql -u%s -p%s -S%s -D%s' % (credentials['user'], credentials['passwd'], credentials['unix_socket'], db), stdout=PIPE, stdin=PIPE, shell=True)
    out = process1.communicate('source ' + rest_file)
    out

print '-' * 60
print '%-15s : %-20s' % ('user', 'host')
print '-' * 60
# Restoreing mysql schema first.
lst = []
ndic = {}
for file in files:
    if file.startswith('mysql'):
        rest_file = os.path.join(dir_path + '/' + file)
        process = Popen('mysql -u%s -p%s -S%s' % (credentials['user'], credentials['passwd'], credentials['unix_socket']), stdout=PIPE, stdin=PIPE, shell=True)
        out = process.communicate('select user, host from mysql.user;')
        db, host = out
        data = db.split()
        print ''
        user = [data[x] for x in range(0, len(data), 2)]
        for host in data:
            if host not in user:
                lst.append(host)
        ndic = dict(zip(user, lst))
        for key, val in ndic.items():
            print '%-15s : %-5s '% (key, val)