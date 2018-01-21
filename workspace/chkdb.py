#!/usr/bin/python

import MySQLdb
user = raw_input('user name: ')
hostname_or_ip = raw_input('hostname or ip: ')
db = raw_input('databse name: ')

if len(user) == 0 : user = 'sunny'
if len(hostname_or_ip) == 0 : hostname_or_ip = '172.16.130.168'
if len(db) == 0 : db = 'testdb' 
print user
print hostname_or_ip
print db
try:
    db = MySQLdb.connect(hostname_or_ip, user, "abc123", db)
except:
    print 'hostname or ip is invalid!'
    exit()

cur = db.cursor()
cur.execute('show variables like "version"')
results = cur.fetchall()

for row in cur:
    print row

db.close()
