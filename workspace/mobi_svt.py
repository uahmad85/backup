#!/usr/bin/python
# SVT tasks

import string
import getpass
from xml.dom import minidom
from fabric.api import hide, sudo, local, run, settings, env, task, puts, runs_once
from fabric.colors import *
from fabric.operations import put, get, sudo, open_shell
from fabric.context_managers import cd, lcd
from fabric.contrib.files import exists, append
from fabric.decorators import with_settings
from mobi_config import loadconfig
import requests
import yaml
import os
import re

@task()
def stmxl_logs():
    """
    tail stmxl logs
    """
    env.warn_only = True
    env.remote_interrupt = True
    sudo("tail -f /var/log/mobi-livesegmenter/livesegmenter.log")
    sudo("tail -f  /var/log/mobi-catchupwriter/catchupwriter.log")
    sudo("tail -f /var/log/mobi-catchupcleaner/catchupcleaner.log")
    sudo("tail -f /var/log/mobi-mediamuxer/mobi-mediamuxer.log")
    sudo("tail -f /var/log/mobi-drmproxy/drmproxy.log")

@task()
def stmxv_logs():
    """
    review stmxv logs
    """
    env.warn_only = True
    env.remote_interrupt = True
    sudo("tail -f /var/log/mobi-mediamuxer/mobi-mediamuxer.log")
    sudo("tail -f /var/log/mobi-drmproxy/drmproxy.log")

@task()
def stdps_logs():
    """
    review stdps logs
    """
    env.warn_only = True
    env.remote_interrupt = True
    sudo("tail -f /var/log/mobi-deployment-server/deploymentserver.log")
    sudo("tail -f /var/log/mobi-solrproxy/solrproxy.log")

@task()
def judrm_logs():
    """
    review judrm logs
    """
    env.warn_only = True
    env.remote_interrupt = True
    sudo("tail -f /var/log/drm/licensemanager2/licensemanager.log")
    sudo("tail -f /var/log/drm/roapserver/roapserver.log")
    sudo("tail -f /var/log/drm/ocspresponder/ocspresponder.log")

@task()
def check_amq_http_status(environment):
    """
    juarn node checks
    """
    environment = environment
    staging_msp = "http://juamq01p1.staging-msp.ops.smf1.mobitv:8161/admin/queues.jsp"
    prod_msp = "http://juamq01p1.prod-msp.smf1.mobitv:8161/admin/queues.jsp"
    if environment.lower() == "staging-msp":
        url = staging_msp
    elif environment.lower() == "prod-msp":
        url = prod_msp
    else:
        print "%s is not a defined environment" % (environment)
    try:
        if re.search('^https', url, flags=re.I):
            requests.packages.urllib3.disable_warnings()
        r = requests.head("%s" % (url))
        if r.status_code == 200:
            print "Oh yeah, Oh yeah, http status code is %s for %s" % (r.status_code, url)
        else:
            print "Uh oh, something doesn't looks right, you received a %s http status code" % (r.status_code)
    except requests.ConnectionError:
        print "Something is wrong, Failed to connect to %s" % (url)

@task()
def check_packages(environment, node_type):
    env.warn_only = True
    package_data = yaml.load(file('packages.yaml'))
    for package in package_data[environment][node_type]:
        with hide("everything"):
            status = run("rpm -qa |grep %s" % package)
        if status != package:
            print (red ("%s - fail" % (package)))
        else:
            print (green("%s - pass" % (package)))

@task()
def check_health(environment, node_type):
    env.warn_only = True
    health_check_data = yaml.load(file('health_checks.yaml'))
    for checks in health_check_data[environment][node_type]:
        with hide("everything"):
            print(run("curl %s" % (checks)))

@task()
def mobi_rpm_out(period):
    period = period
    if period == 'before':
        with hide('everything'):
            sudo('rpm -qa |grep mobi* >> /tmp/before_deployment.out')
    else:
        with hide('everything'):
            sudo('rpm -qa |grep mobi* >> /tmp/after_deployment.out')

@task()
def mobi_package_diff():
    env.warn_only = True
    with hide('everything'):
        output = sudo('diff /tmp/before_deployment.out /tmp/after_deployment.out')
        print output
