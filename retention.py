#!/usr/bin/python
import os
import time

backup_store = '/var/mysql_mount/backup'
backups = os.listdir(backup_store)
today = time.time()
three_days = 259200
half_day = 86400   
 
for dirs in backups:
    if (today - os.stat(dirs).st_mtime) > half_day:
        print dirs
        