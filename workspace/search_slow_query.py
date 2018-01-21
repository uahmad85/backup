#!/usr/bin/env python

import argparse
import datetime

parser = argparse.ArgumentParser(description='Usage: ')
parser.add_argument('-f', '--log_file', action='store', default=False, help='log file to parse for queries')
parser.add_argument('-p', '--path', action='store', default=False, help='log file to parse for queries')
parser.add_argument('-d', '--date', action='store', default=False, help='date when the incident happened')
parser.add_argument('-H', '--hour', action='store', default=False, help='hour when the icident happened')
results = parser.parse_args()

log_file = 'slow_query.log'
log_file_path = '/var/log/mongodb'
date = datetime.date.today()
date_isof = date.isoformat()
search_date = date_isof.split('T')[0]
slowest_so_far = 0

if results.log_file:
    log_file = results.log_file

if results.path:
    log_file_path = results.path

if results.date:
    search_date = results.date

if results.hour and results.date:
    search_date = 'T'.join([search_date, results.hour])

print search_date

file_handler = open(log_file_path + '/' + log_file)

for line in file_handler:
    if line.startswith(search_date):
        if 'ms' in line:
            query_time = int(line.split(':')[-1].split()[-1].strip('ms'))
            if query_time > slowest_so_far:
                slowest_so_far = query_time
                print line