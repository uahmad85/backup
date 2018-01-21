#!/usr/bin/python
from shutil import *
import os

for dir, dp, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            print(os.path.join(dir, file))
            copy(dir + '/' + file, '/Users/sunahmad/Documents/workspace/')
