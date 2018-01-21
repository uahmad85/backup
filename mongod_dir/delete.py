#Remove all the directories older than 3 days
import os
from time import time
import re

backups = os.listdir('.')
today = time()
three_days = 259200

#os.chdir(backup_dir)

for files in backups:
  tars = re.findall('\S.*.tar.gz', files)
  enc = re.findall('\S.*.enc', files)
  if len(tars) != 0:
    for tarball in tars:
      if (today - float(os.stat(tarball).st_ctime)) > 10 and (today - float(os.stat(tarball).st_ctime)) > 10:
        print 'Backups marked for deletion: %s, %s' % (tars, enc)
        #os.remove(tarball)

