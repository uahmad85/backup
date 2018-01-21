#!/usr/bin/python

import zipfile
import sys
import os
import logging

bk_file = 'backup.zip'

logging.basicConfig(filename='backup.log', level = logging.DEBUG)

logging.info('checking if the backup file already exists')
if os.path.exists(bk_file):
    logging.info('file %s exists' % (bk_file))
    try:
        zip_file = zipfile.ZipFile(bk_file, 'a')
    except:
        err = sys.exc_info()
        logging.error('unable to open the file %s' % (bk_file))
        logging.error('Error no: ' + str(err[1].args[0]))
        logging.error('Error meg: ' + str(err))
        sys.exit()
else:
    try:
        zip_file = zipfile.ZipFile(bk_file, 'w')
    except:
        err = sys.exc_info()
        logging.error('unable to create the file %s' % (bk_file))
        logging.error('Error no: ' + str(err[1].args[0]))
        logging.error('Error meg: ' + err[1].args[1])
        sys.exit()
try:
    logging.info('adding test.txt file to backup.zip')
    zip_file.write('test2.txt', zipfile.ZIP_DEFLATED)
except:
    err = sys.exc_info()
    logging.error('unable to add the file %s' % (bk_file))
    logging.error('Error no: ' + str(err[1].args[0]))
    logging.error('Error meg: ' + str(err))

zip_file.close()
