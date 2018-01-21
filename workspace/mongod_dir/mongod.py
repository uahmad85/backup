#!/usr/bin/python

import re
import os
import sys
import argparse
from shutil import *
from time import strftime, time
from subprocess import Popen, call, PIPE, CalledProcessError

import boto3


parser = argparse.ArgumentParser(description='Usage: to index all the users or items ./index.py [ --user | --item ]')
parser.add_argument('-a', '--addoptions', action='store', default=False, help='to pass any optional arguments to mongo')
parser.add_argument('-bd', '--backupdir', action='store', default=False, help='Directory to store the backups')
parser.add_argument('-s3', '--s3bucket', action='store', default=False, help='to pass any optional arguments to mongo')
results = parser.parse_args()
print results

s3 = boto3.resource('s3')
s3_bucket = 'close5-backupsforecg'
date = strftime('%Y%m%d-%H%M')
backup_file = 'backup-' + date + '.tar.gz'
backup_data_dir = '/Users/sunahmad/Documents/workspace/mongod_dir/dump'
backup_tar_files_dir = '/Users/sunahmad/Documents/workspace/mongod_dir'
options = ''
today = time()
three_days = 259200
if results.addoptions:
  options = results.addoptions

if results.backupdir:
  backup_data_dir = results.backupdir

if results.s3bucket:
  s3_bucket = results.s3bucket

if not os.path.isdir(backup_data_dir):
  os.makedirs(backup_data_dir)


try:
  process = Popen('mongodump --gzip %s -o %s' % (options, backup_data_dir), shell=True).communicate()[0]
  process = Popen('tar -cvzf %s %s' % (backup_file, 'dump'), shell=True).communicate()[0]
  rmtree(backup_data_dir)
except CalledProcessError as err:
  print(err)
  sys.exit()

s3.meta.client.upload_file(backup_file, s3_bucket, backup_file)

#Remove all the directories older than 3 days

os.chdir(backup_tar_files_dir)
backups = os.listdir('.')

for files in backups:
  tars = re.findall('\S.*.tar.gz', files)
  if len(tars) != 0:
    for tarball in tars:
      if today - float(os.stat(tarball).st_ctime) > 1200:
        print 'Backups marked for deletion: %s' % (tarball)
        os.remove(tarball)
