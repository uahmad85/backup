#!/usr/bin/python

import sys
import os

try:
    os.execl('/bin/ls', ['test', 'testing', 'testted'])
except OSError:
    print 'file doesnt exist!'
    print os.strerror(OSError)
