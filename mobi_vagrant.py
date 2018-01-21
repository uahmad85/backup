#!/usr/bin/python
#
# Mobi Adminstration tasks

from fabric.api import hide, sudo, local, run, settings, env, task, puts
from fabric.colors import *
from fabric.operations import put, get, sudo, open_shell
from fabric.context_managers import cd, lcd
from fabric.contrib.files import exists, append
from fabric.decorators import with_settings

@task()
def vagrant_up: