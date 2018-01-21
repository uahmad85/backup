#!/usr/bin/python
#
# Mobi Adminstration tasks

import urllib
import crypt
from random import choice, randint, getrandbits
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
import re
import yaml
import os


@task
def random_password(length=10,output=True):
    """
    Generate random password
    """
    pw = ''.join(choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(int(length)))
    if output:
        puts(green(pw))
        return 0

    return pw

@task
def memcached_restart():
    """
    Memcached service restart
    """
    sudo("service memcached restart")

@task
def memcached_status():
    """
    Memcached service status
    """
    sudo("service memcached restart")

@task(alias='yc')
def yum_clean():
    """
    Clean yum repos
    """
    sudo("yum clean all")

@task
def yum_remove_rpm(rpmname):
    """
    Remove RPM 
    """
    sudo('yum -y remove %s' % (rpmname))
    
@task
def remove_rpm(rpmname):
    """
    Remove RPM 
    """
    sudo('rpm -e  %s' % (rpmname))
    
    
@task
def change_file_owner_and_group(owner, file):
    """
    Change file owner ad group 
    """
    sudo('chown %s %s' % (owner) % (file))

@task
def grep_log(grep_string, log_file):
    """
    Grep logs: fab -H 10.x.x.x check_puppet_run:'your string','/var/lib/puppet/state/last_run_summary.yaml'
    """
    sudo('grep -i %s %s' % (grep_string, log_file))

@task(alias='lmp')
def ls_mobi_packages():
    """
    List mobitv packages
    """
    sudo("rpm -qa |grep -i mobi |sort")

@task
def rabbitmq_cmd(cmd):
    """
    run rabbitmqctl command on server. fab -H x.x.x.x rabbitmq_cmd:list_queues
    """
    sudo('rabbitmqctl %s' % (cmd))

@task(alias='lls')
def ls_log_size(directory, log_size):
    """
    ls file sizes in a dir on a server. fab -l 10.x.x.x ls_log_size:'/var/log/',100000
    """
    sudo('find %s -type f -size +%sk -exec ls -lh {} \; | awk \'{print $9 ":" $5}\'' % (directory, log_size))

@task
def ls_log_days(directory, log_days):
    """
    ls file sizes in a dir on a server. fab -l 10.x.x.x ls_log_size:'/var/log/',14
    """
    sudo('find %s -type f -mtime +%s -exec ls -lh {} \;' % (directory, log_days))

@task
def get_lab_ips(number_ips, vlan_tag):
    """
    Check for available ip's: fab get_ips:'<number of ip's>','<vlan tag>'
    """
    local('curl "http://navrav.qa.smf1.mobitv/vms/getIPs?num_of_ips=%s&vlan=%s"' % (number_ips, vlan_tag))

@task
def get_prod_ips(number_ips, vlan_tag):
    """
    Check for available ip's: fab get_ips:'<number of ip's>','<vlan tag>'
    """
    local('curl "http://navrav.prod-msp.smf1.mobitv/vms/getIPs?num_of_ips=%s&vlan=%s"' % (number_ips, vlan_tag))

@task(alias='ts')
def tomcat_status():
    """
    Check Tomcat status
    """
    sudo('/etc/init.d/tomcat8080 status')

@task
def tomcat_stop():
    """
    Stop Tomcat
    """
    env.warn_only
    sudo('/etc/init.d/tomcat8080 stop')

@task
def tomcat_restart():
    """
    Restart Tomcat
    """
    sudo('/etc/init.d/tomcat8080 restart')

@task
def tomcat_start():
    """
    Start Tomcat
    """
    sudo('/etc/init.d/tomcat8080 start')

@task
def jetspeed_stop():
    """
    Stop jetspeed
    """
    sudo('/etc/init.d/jetspeed stop')

@task
def jetspeed_restart():
    """
    Restart jetspeed
    """
    sudo('/etc/init.d/jetspeed restart')

@task
def jetspeed_start():
    """
    Start jetspeed
    """
    sudo('/etc/init.d/jetspeed start')


@task
def solr_stop():
    """
    Stop SOLR
    """
    sudo('/etc/init.d/solr stop')

@task
def solr_start():
    """
    Stop SOLR
    """
    sudo('/etc/init.d/solr start')

@task
def activemq_stop():
    """
    Stop ActiveMQ
    """
    sudo('/etc/init.d/activemq stop')

@task
def activemq_start():
    """
    Stop ActiveMQ
    """
    sudo('/etc/init.d/activemq start')

@task
def ftplogparser_stop():
    """
    Stop ftplogparser
    """
    sudo('/etc/init.d/mobi-cms-ftplogparser stop')

@task
def livesegmenter_stop():
    """
    Stop livesegmenter
    """
    sudo('/etc/init.d/livesegmenter stop')

@task
def livesegmenter_start():
    """
    Start livesegmenter
    """
    sudo('/etc/init.d/livesegmenter start')

@task
def ftplogparser_start():
    """
    Start ftplogparser
    """
    sudo('/etc/init.d/mobi-cms-ftplogparser start')

@task
def httpd_stop():
    """
    Stop httpd (apache)
    """
    sudo('/etc/init.d/httpd stop')

@task
def httpd_start():
    """
    Start httpd (apache)
    """
    sudo('/etc/init.d/httpd start')

@task
def httpd_restart():
    """
    restart httpd (apache)
    """
    sudo('/etc/init.d/httpd restart')

@task
def varnish_stop():
    """
    Stop varnish
    """
    sudo('/etc/init.d/varnish stop')

@task
def varnish_start():
    """
    Start varnish
    """
    sudo('/etc/init.D/varnish start')

@task
def varnishncsa_stop():
    """
    Stop varnishncsa
    """
    sudo('/etc/init.d/varnishncsa stop')

@task
def varnishncsa_start():
    """
    Start varnishnsca
    """
    sudo('/etc/init.d/varnishncsa start')


@task
def sudo_run_command(cmd):
    """
    Run command as root
    """
    sudo('%s' % (cmd))

@task
def run_command(cmd):
    """
    Run command as user
    """
    run('%s' % (cmd))

@task()
def run_vmware_shell_command(cmd):
    """
    Run command as root on vxhost
    """
    env.user = 'root'
    env.password = 'm0b1r0ck5!'
    env.shell = "/bin/sh -c"
    run('%s' % (cmd))

@task
def vm_remove_snapshots():
    """
    Delete vm snapshots
    """
    env.user = 'root'
    env.password = 'm0b1r0ck5!'
    env.shell = "/bin/sh -c"
    runs_once('/bin/sh ./removesnap.sh')

@task
def vm_create_snapshots():
    """
    Delete vm snapshots
    """
    env.user = 'root'
    env.password = 'm0b1r0ck5!'
    env.shell = "/bin/sh -c"
    runs_once('/bin/sh ./createsnap.sh')

@task
def amq_master():
    """
    Get amq master
    """
    sudo('tail /var/log/activemq/activemq.log')

@task
def check_gm(yaml_dir):
    """
    Verify rpm exist: fab -H <hosts> mobi_admin.check_gm:'<yaml_dir>'
    """
    env.warn_only
    yaml_dir = yaml_dir
    yaml_files = os.listdir(yaml_dir)

    for f in yaml_files:
        yaml_file = yaml_dir + f
        yaml_data = yaml.load(file(yaml_file))
        parse_file = re.sub(r'\.yaml$', '', f)
        try:
            package_name = "%s::package" % (parse_file)
            package_version = yaml_data[package_name]["ensure"]
        except:
            print "Package not defined: %s" % (yaml_file)
        sudo("yum list %s-%s --showduplicates" % (parse_file, package_version))

@task(alias='cyf')
def check_yaml_file(yaml_file):
    """
    verify yaml file syntax
    """
    env.warn_only
    local("ruby -e \"require 'yaml'; YAML.load_file('%s')\"" % (yaml_file))

@task(alias='cyd')
def check_yaml_dir(yaml_dir):
    """
    verify yaml syntax on all yaml files in a dir
    """
    env.warn_only
    yaml_dirs = os.walk(yaml_dir)
    for d in yaml_dirs:
        yaml_files = [f for f in os.listdir(d[0]) if os.path.isfile("%s/%s" % (d[0], f))]
        yaml_dir = d[0]
        for yaml_file in yaml_files:
            if yaml_file.endswith('.yaml'):
                full_path = "%s/%s" % (yaml_dir, yaml_file)
                local("ruby -e \"require 'yaml'; YAML.load_file('%s')\"" % (full_path))

@task
def hello():
    """hello world - uname; whoami; date; uptime"""
    run('uname -a ; whoami; date; uptime')
