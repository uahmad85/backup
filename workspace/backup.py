#!/usr/bin/python

import os
import sys
from shutil import *
from time import strftime, time
from subprocess import Popen, call, PIPE
from ConfigParser import SafeConfigParser

import _mysql
import _mysql_exceptions

parser = SafeConfigParser()
if not os.path.isfile('.credentials'):
    print 'Error: Credentials file not found! Please make sure .credentials file is present.'
    sys.exit()

parser.read('.credentials')
lst = []
credentials = {}

options = '--opt --skip-lock-tables --single-transaction --skip-events'
mount_dir = '/var/mysql_mount'
date = strftime('%Y%m%d-%H%M')
backup_dir = mount_dir + '/backup'
sql_gz = date + '.sql.gz'
avoid_db = (('information_schema',),('performance_schema',))

for instance in parser.sections():
    instance_dir = backup_dir + '/' + date + '/' + instance
    if not os.path.isdir(instance_dir) : os.makedirs(instance_dir)
    for key, val in parser.items(instance):
        credentials[key] = val

    print instance
    try:
        db_con = _mysql.connect(**credentials)
    except _mysql_exceptions.OperationalError as myerr:
        print myerr
        print "Please check your username and password in /home/devops/.credentials file!"
        sys.exit()
    db_con.query("show databases;")
    result = db_con.store_result()
    for all_db in result.fetch_row(0):
        if all_db not in avoid_db:
            for db in all_db:
                try:
                    print 'mysqldump -u%s -p%s -S%s %s %s | gzip > %s/%s-%s' % (credentials['user'], credentials['passwd'],credentials['unix_socket'], options, db, instance_dir, db, sql_gz)
                    process = Popen('mysqldump -u%s -p%s -S%s %s %s | gzip > %s/%s-%s' % (credentials['user'], credentials['passwd'],credentials['unix_socket'], options, db, instance_dir, db, sql_gz), stdout=PIPE, shell=True).communicate()
                    process
                    os.listdir(instance_dir)
                except _mysql_exceptions.OperationalError as myerr:
                    print myerr
                    sys.exit()

#Remove all the directories older than 3 days

backups = os.listdir(backup_dir)
today = time()
three_days = 259200

os.chdir(backup_dir)

for dirs in backups:
    if today - float(os.stat(dirs).st_ctime) > three_days:
        print 'Backups marked for deletions: %s' % (dirs)
        print rmtree(dirs)
        print rmtree(dirs)
