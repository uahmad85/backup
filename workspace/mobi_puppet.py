#!/usr/bin/python
#
# Puppet tasks

from fabric.api import hide, sudo, local, run, settings, env, task, puts
from fabric.colors import *
from fabric.operations import put, get, sudo, open_shell
from fabric.context_managers import cd, lcd
from fabric.contrib.files import exists, append
from fabric.decorators import with_settings
from fabric.colors import red, green
import os


@task(alias='rp')
def run_puppet():
    """
    Run puppet agent
    """
    with settings(hide('everything'),
                  warn_only=True
                  ):
        return sudo("puppet agent -tv |grep -i error")

@task(alias='stp')
def stop_puppet():
    """
    Stop puppet agent
    """
    with settings(warn_only=True):
        return sudo("/etc/init.d/puppet stop")
        
@task(alias='sts')
def check_puppet_status():
    """
    Check puppet agent status
    """
    with settings(warn_only=True):
        return sudo("/etc/init.d/puppet status")
       

@task
def pm_cert_list():
    """
    PuppetMaster ssl cert list
    """
    sudo("puppet cert list --all")

@task
def remove_puppet_ssl():
    """
    Remove ssl certs from a puppet client
    """
    sudo("rm -rf /var/lib/puppet/ssl/*")

@task(alias='pcc')
def puppet_cert_clean(server):
    """
    Remove ssl certs from  puppet master
    """
    sudo("puppet node clean %s" % (server))
    
@task
def puppet_master_nodes_deactivate(nodes):
    """
    Deactivate node from puppet master
    """
    sudo("puppet node deactivate %s" % (nodes))
    
@task
def set_agent_puppetmaster_and_env(fqdn, env):
    """
    Set the agent's puppet master and environment (the mobi-puppet branch)
    """
    sudo('mkdir -p  /tmp')
    put("./startup_script.sh","/tmp/startup_script.sh", use_sudo=True)
    sudo('chmod +x /tmp/startup_script.sh')
    sudo("cd /tmp && ./startup_script.sh " + fqdn + " " + env)

@task(alias='upm')
def update_puppet_master(puppet_module, puppet_branch):
    """
    Run after committing your changes to module repo. fab update_puppet_master:yum,func_msp_qa_smf1_mobitv
    """
    run('curl -i http://inrcs01.ci-infra.devops.smf1.mobitv/deploy_modules?modules=%s&branch=%s' % (puppet_module, puppet_branch))

@task
def remove_facter():
    """
    Remove facter
    """
    sudo('yum -y remove facter')

@task
def create_facter_dir():
    """
    Create facter directory
    """
    sudo('mkdir -p /etc/facter/facts.d')

@task
def install_puppet():
    """
    Install puppet 3.1
    """
    sudo('yum -y install puppet-3.1.1-1.el6 facter-1.7.4-1.el6')

@task
def add_puppet_conf(platform):
    """
    Put node type file on server "add_puppet_conf:ci-cp"
    """
    if platform == "ci-cp":
        put('files/puppet_ci_cp.conf', '/etc/puppet/puppet.conf', use_sudo=True, mode=755)
    elif platform == "func-cp":
        put('files/puppet_func_cp.conf', '/etc/puppet/puppet.conf', use_sudo=True, mode=755)
    elif platform == "ppd-cp":
        put('files/puppet_ppd_cp.conf', '/etc/puppet/puppet.conf', use_sudo=True, mode=755)
    elif platform == "staging-msp":
        put('files/puppet_staging_msp.conf', '/etc/puppet/puppet.conf', use_sudo=True, mode=755)
    elif platform == "prod-msp":
        put('files/puppet_prod_msp.conf', '/etc/puppet/puppet.conf', use_sudo=True, mode=755)
    elif platform == "prodeast-msp":
        put('files/puppet_prodeast_msp.conf', '/etc/puppet/puppet.conf', use_sudo=True, mode=755)
    elif platform == "integration-msp":
        put('files/puppet_integration_msp.conf', '/etc/puppet/puppet.conf', use_sudo=True, mode=755)
    else:
        print "Please specify a platform: ci-cp, func-cp, ppd-cp, etc... "

@task
def add_node_type():
    """
    Install puppet 3.1
    """
    put('files/node_type.py', '/etc/facter/facts.d/', use_sudo=True, mode=755)

@task
def last_run():
    """
    Check puppet last run for Success and Failures
    """
    with hide("everything"):
       report = sudo('grep -A4 -i events /var/lib/puppet/state/last_run_summary.yaml')
       print(report)
