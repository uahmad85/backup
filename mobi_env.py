#!/usr/bin/python
#
# Define environments

from fabric.api import env, hosts, roles
from fabric.api import hide, sudo, local, run, settings, env, task, puts
import sys
from pypuppetdb import connect
from mobi_config import loadconfig

# Load credentials config file if available.
#credentials.cfg
# [user]
# user = username
# password = password
try:
 credentials = loadconfig('credentials')
 env.user = credentials.get('user', 'user')
 env.password = credentials.get('user', 'password')
except:
    print 'Add a credentials.cfg with your user name and password: https://confluence.mobitv.corp/display/DEVOPS/devop_fab'

# create role groups manually if you can not query the node type from puppetdb.
env.roledefs = {
    ### PPD MSP
 'dbmgt-ppd-msp': ['dbmgt01p1.staging-msp.ops.smf1.mobitv'],
 'ingan-ppd-msp': ['ingan01p1.staging-msp.ops.smf1.mobitv'],
 'inicg-ppd-msp': ['inicg01p1.staging-msp.ops.smf1.mobitv'],
 'inldp-ppd-msp': [ 'inldp01p1.staging-msp.ops.smf1.mobitv', 'inldp02p1.staging-msp.ops.smf1.mobitv'],
 'juamq-ppd-msp': [ 'juamq01p1.staging-msp.ops.smf1.mobitv',  'juamq02p1.staging-msp.ops.smf1.mobitv'],
 'juarn-ppd-msp': [ 'juarn01p1.staging-msp.ops.smf1.mobitv',  'juarn02p1.staging-msp.ops.smf1.mobitv'],
 'judrm-ppd-msp': [ 'judrm01p1.staging-msp.ops.smf1.mobitv',  'judrm02p1.staging-msp.ops.smf1.mobitv'],
 'juing-ppd-msp': [ 'juing01p1.staging-msp.ops.smf1.mobitv',  'juing02p1.staging-msp.ops.smf1.mobitv'],
 'jupkg-ppd-msp': [ 'jupkg01p1.staging-msp.ops.smf1.mobitv',  'jupkg02p1.staging-msp.ops.smf1.mobitv'],
 'msamq-ppd-msp': [ 'msamq01p1.staging-msp.ops.smf1.mobitv',  'msamq02p1.staging-msp.ops.smf1.mobitv'],
 'msath-ppd-msp': [ 'msath01p1.staging-msp.ops.smf1.mobitv',  'msath02p1.staging-msp.ops.smf1.mobitv'],
 'msepg-ppd-msp': [ 'msepg01p1.staging-msp.ops.smf1.mobitv',  'msepg02p1.staging-msp.ops.smf1.mobitv'],
 'msfrn-ppd-msp': [ 'msfrn01p1.staging-msp.ops.smf1.mobitv',  'msfrn02p1.staging-msp.ops.smf1.mobitv'],
 'msliv-ppd-msp': [ 'msliv01p1.staging-msp.ops.smf1.mobitv',  'msliv02p1.staging-msp.ops.smf1.mobitv'],
 'msnom-ppd-msp': [ 'msnom01p1.staging-msp.ops.smf1.mobitv',  'msnom02p1.staging-msp.ops.smf1.mobitv'],
 'msofm-ppd-msp': [ 'msofm01p1.staging-msp.ops.smf1.mobitv',  'msofm02p1.staging-msp.ops.smf1.mobitv'],
 'msprf-ppd-msp': [ 'msprf01p1.staging-msp.ops.smf1.mobitv',  'msprf02p1.staging-msp.ops.smf1.mobitv'],
 'msqov-ppd-msp': [ 'msqov01p1.staging-msp.ops.smf1.mobitv'],
 'mssch-ppd-msp': [ 'mssch01p1.staging-msp.ops.smf1.mobitv',  'mssch02p1.staging-msp.ops.smf1.mobitv'],
 'mssub-ppd-msp': [ 'mssub01p1.staging-msp.ops.smf1.mobitv',  'mssub02p1.staging-msp.ops.smf1.mobitv'],
 'msxmp-ppd-msp': [ 'msxmp01p1.staging-msp.ops.smf1.mobitv',  'msxmp02p1.staging-msp.ops.smf1.mobitv'],
 'mszoo-ppd-msp': [ 'mszoo01p1.staging-msp.ops.smf1.mobitv',  'mszoo02p1.staging-msp.ops.smf1.mobitv',  'mszoo03p1.staging-msp.ops.smf1.mobitv'],
 'nocas-ppd-msp': [ 'nocas01p1.staging-msp.ops.smf1.mobitv',  'nocas02p1.staging-msp.ops.smf1.mobitv',  'nocas03p1.staging-msp.ops.smf1.mobitv'],
 'noslr-old-ppd-msp': [ 'noslr01p1.staging-msp.ops.smf1.mobitv',  'noslr02p1.staging-msp.ops.smf1.mobitv'],
 'noslr-new-ppd-msp': [ 'noslr03p1.staging-msp.ops.smf1.mobitv', 'noslr04p1.staging-msp.ops.smf1.mobitv','noslr05p1.staging-msp.ops.smf1.mobitv'],
 'sqdtb-old-ppd-msp': [ 'sqdtb01p1.staging-msp.ops.smf1.mobitv',  'sqdtb02p1.staging-msp.ops.smf1.mobitv'],
 'sqdtb-new-ppd-msp': [ 'sqdtb03p1.staging-msp.ops.smf1.mobitv',  'sqdtb04p1.staging-msp.ops.smf1.mobitv'],
 'stdps-ppd-msp': [ 'stdps01p1.staging-msp.ops.smf1.mobitv',  'stdps02p1.staging-msp.ops.smf1.mobitv','stdps01p2.staging-msp.ops.smf1.mobitv',  'stdps02p2.staging-msp.ops.smf1.mobitv'],
 'stmxl-ppd-msp': [ 'stmxl01p1.staging-msp.ops.smf1.mobitv',  'stmxl02p1.staging-msp.ops.smf1.mobitv', 'stmxl03p1.staging-msp.ops.smf1.mobitv',  'stmxl04p1.staging-msp.ops.smf1.mobitv', 'stmxl05p1.staging-msp.ops.smf1.mobitv',  'stmxl06p1.staging-msp.ops.smf1.mobitv'],
 'stmxv-ppd-msp': [ 'stmxv01p1.staging-msp.ops.smf1.mobitv',  'stmxv02p1.staging-msp.ops.smf1.mobitv'],
##'stsgl-ppd-msp': [ 'stsgl01p1.staging-msp.ops.smf1.mobitv',  'stsgl02p1.staging-msp.ops.smf1.mobitv'],
 'stval-ppd-msp': [ 'stval01p1.staging-msp.ops.smf1.mobitv',  'stval02p1.staging-msp.ops.smf1.mobitv'],
 'stvav-ppd-msp': [ 'stvav01p1.staging-msp.ops.smf1.mobitv',  'stvav02p1.staging-msp.ops.smf1.mobitv'],
 'svcar-ppd-msp': ['svcar01p1.staging-msp.ops.smf1.mobitv',   'svcar02p1.staging-msp.ops.smf1.mobitv'],
 'svdtm-ppd-msp': ['svdtm01p1.staging-msp.ops.smf1.mobitv',   'svdtm02p1.staging-msp.ops.smf1.mobitv'],
 'svftp-ppd-msp': ['svftp01p1.staging-msp.ops.smf1.mobitv',   'svftp02p1.staging-msp.ops.smf1.mobitv'],
 'svmgt-ppd-msp': [ 'svmgt01p1.staging-msp.ops.smf1.mobitv'],
    ### PPD MSP
 'dbmgt-ppd-msp': ['dbmgt01p1.ppd-msp.qa.smf1.mobitv'],
 'ingan-ppd-msp': ['ingan01p1.ppd-msp.qa.smf1.mobitv'],
 'inicg-ppd-msp': ['inicg01p1.ppd-msp.qa.smf1.mobitv'],
 'inldp-ppd-msp': [ 'inldp01p1.ppd-msp.qa.smf1.mobitv', 'inldp02p1.ppd-msp.qa.smf1.mobitv'],
 'juamq-ppd-msp': [ 'juamq01p1.ppd-msp.qa.smf1.mobitv',  'juamq02p1.ppd-msp.qa.smf1.mobitv'],
 'juarn-ppd-msp': [ 'juarn01p1.ppd-msp.qa.smf1.mobitv',  'juarn02p1.ppd-msp.qa.smf1.mobitv'],
 'judrm-ppd-msp': [ 'judrm01p1.ppd-msp.qa.smf1.mobitv',  'judrm02p1.ppd-msp.qa.smf1.mobitv'],
 'juing-ppd-msp': [ 'juing01p1.ppd-msp.qa.smf1.mobitv',  'juing02p1.ppd-msp.qa.smf1.mobitv'],
 'jupkg-ppd-msp': [ 'jupkg01p1.ppd-msp.qa.smf1.mobitv',  'jupkg02p1.ppd-msp.qa.smf1.mobitv'],
 'msamq-ppd-msp': [ 'msamq01p1.ppd-msp.qa.smf1.mobitv',  'msamq02p1.ppd-msp.qa.smf1.mobitv'],
 'msath-ppd-msp': [ 'msath01p1.ppd-msp.qa.smf1.mobitv',  'msath02p1.ppd-msp.qa.smf1.mobitv'],
 'msepg-ppd-msp': [ 'msepg01p1.ppd-msp.qa.smf1.mobitv',  'msepg02p1.ppd-msp.qa.smf1.mobitv'],
 'msfrn-ppd-msp': [ 'msfrn01p1.ppd-msp.qa.smf1.mobitv',  'msfrn02p1.ppd-msp.qa.smf1.mobitv'],
 'msliv-ppd-msp': [ 'msliv01p1.ppd-msp.qa.smf1.mobitv',  'msliv02p1.ppd-msp.qa.smf1.mobitv'],
 'msnom-ppd-msp': [ 'msnom01p1.ppd-msp.qa.smf1.mobitv',  'msnom02p1.ppd-msp.qa.smf1.mobitv'],
 'msofm-ppd-msp': [ 'msofm01p1.ppd-msp.qa.smf1.mobitv',  'msofm02p1.ppd-msp.qa.smf1.mobitv'],
 'msprf-ppd-msp': [ 'msprf01p1.ppd-msp.qa.smf1.mobitv',  'msprf02p1.ppd-msp.qa.smf1.mobitv'],
 'msqov-ppd-msp': [ 'msqov01p1.ppd-msp.qa.smf1.mobitv'],
 'mssch-ppd-msp': [ 'mssch01p1.ppd-msp.qa.smf1.mobitv',  'mssch02p1.ppd-msp.qa.smf1.mobitv'],
 'mssub-ppd-msp': [ 'mssub01p1.ppd-msp.qa.smf1.mobitv',  'mssub02p1.ppd-msp.qa.smf1.mobitv'],
 'msxmp-ppd-msp': [ 'msxmp01p1.ppd-msp.qa.smf1.mobitv',  'msxmp02p1.ppd-msp.qa.smf1.mobitv'],
 'mszoo-ppd-msp': [ 'mszoo01p1.ppd-msp.qa.smf1.mobitv',  'mszoo02p1.ppd-msp.qa.smf1.mobitv',  'mszoo03p1.ppd-msp.qa.smf1.mobitv'],
 'nocas-ppd-msp': [ 'nocas01p1.ppd-msp.qa.smf1.mobitv',  'nocas02p1.ppd-msp.qa.smf1.mobitv',  'nocas03p1.ppd-msp.qa.smf1.mobitv'],
 'noslr-old-ppd-msp': [ 'noslr01p1.ppd-msp.qa.smf1.mobitv',  'noslr02p1.ppd-msp.qa.smf1.mobitv'],
 'noslr-new-ppd-msp': [ 'noslr03p1.ppd-msp.qa.smf1.mobitv', 'noslr04p1.ppd-msp.qa.smf1.mobitv','noslr05p1.ppd-msp.qa.smf1.mobitv'],
 'sqdtb-old-ppd-msp': [ 'sqdtb01p1.ppd-msp.qa.smf1.mobitv',  'sqdtb02p1.ppd-msp.qa.smf1.mobitv'],
 'sqdtb-new-ppd-msp': [ 'sqdtb03p1.ppd-msp.qa.smf1.mobitv',  'sqdtb04p1.ppd-msp.qa.smf1.mobitv'],
 'stdps-ppd-msp': [ 'stdps01p1.ppd-msp.qa.smf1.mobitv',  'stdps02p1.ppd-msp.qa.smf1.mobitv','stdps01p2.ppd-msp.qa.smf1.mobitv',  'stdps02p2.ppd-msp.qa.smf1.mobitv'],
 'stmxl-ppd-msp': [ 'stmxl01p1.ppd-msp.qa.smf1.mobitv',  'stmxl02p1.ppd-msp.qa.smf1.mobitv'],
 'stmxv-ppd-msp': [ 'stmxv01p1.ppd-msp.qa.smf1.mobitv',  'stmxv02p1.ppd-msp.qa.smf1.mobitv'],
##'stsgl-ppd-msp': [ 'stsgl01p1.ppd-msp.qa.smf1.mobitv',  'stsgl02p1.ppd-msp.qa.smf1.mobitv'],
 'stval-ppd-msp': [ 'stval01p1.ppd-msp.qa.smf1.mobitv',  'stval02p1.ppd-msp.qa.smf1.mobitv'],
 'stvav-ppd-msp': [ 'stvav01p1.ppd-msp.qa.smf1.mobitv',  'stvav02p1.ppd-msp.qa.smf1.mobitv'],
 'svcar-ppd-msp': ['svcar01p1.ppd-msp.qa.smf1.mobitv',   'svcar02p1.ppd-msp.qa.smf1.mobitv'],
 'svdtm-ppd-msp': ['svdtm01p1.ppd-msp.qa.smf1.mobitv',   'svdtm02p1.ppd-msp.qa.smf1.mobitv'],
 'svftp-ppd-msp': ['svftp01p1.ppd-msp.qa.smf1.mobitv',   'svftp02p1.ppd-msp.qa.smf1.mobitv'],
 'svmgt-ppd-msp': [ 'svmgt01p1.ppd-msp.qa.smf1.mobitv'],

    ### FUNC MSP
 'dbmgt-func-msp': ['dbmgt01p1.func-msp.qa.smf1.mobitv'],
 'ingan-func-msp': ['ingan01p1.func-msp.qa.smf1.mobitv'],
 'inicg-func-msp': ['inicg01p1.func-msp.qa.smf1.mobitv'],
 'inldp-func-msp': [ 'inldp01p1.func-msp.qa.smf1.mobitv', 'inldp02p1.func-msp.qa.smf1.mobitv'],
 'juamq-func-msp': [ 'juamq01p1.func-msp.qa.smf1.mobitv',  'juamq02p1.func-msp.qa.smf1.mobitv'],
 'juarn-func-msp': [ 'juarn01p1.func-msp.qa.smf1.mobitv',  'juarn02p1.func-msp.qa.smf1.mobitv'],
 'judrm-func-msp': [ 'judrm01p1.func-msp.qa.smf1.mobitv',  'judrm02p1.func-msp.qa.smf1.mobitv'],
 'juing-func-msp': [ 'juing01p1.func-msp.qa.smf1.mobitv',  'juing02p1.func-msp.qa.smf1.mobitv'],
 'jupkg-func-msp': [ 'jupkg01p1.func-msp.qa.smf1.mobitv',  'jupkg02p1.func-msp.qa.smf1.mobitv'],
 'msamq-func-msp': [ 'msamq01p1.func-msp.qa.smf1.mobitv',  'msamq02p1.func-msp.qa.smf1.mobitv'],
 'msath-func-msp': [ 'msath01p1.func-msp.qa.smf1.mobitv',  'msath02p1.func-msp.qa.smf1.mobitv'],
 'msepg-func-msp': [ 'msepg01p1.func-msp.qa.smf1.mobitv',  'msepg02p1.func-msp.qa.smf1.mobitv'],
 'msfrn-func-msp': [ 'msfrn01p1.func-msp.qa.smf1.mobitv',  'msfrn02p1.func-msp.qa.smf1.mobitv'],
 'msliv-func-msp': [ 'msliv01p1.func-msp.qa.smf1.mobitv',  'msliv02p1.func-msp.qa.smf1.mobitv'],
 'msnom-func-msp': [ 'msnom01p1.func-msp.qa.smf1.mobitv',  'msnom02p1.func-msp.qa.smf1.mobitv'],
 'msofm-func-msp': [ 'msofm01p1.func-msp.qa.smf1.mobitv',  'msofm02p1.func-msp.qa.smf1.mobitv'],
 'msprf-func-msp': [ 'msprf01p1.func-msp.qa.smf1.mobitv',  'msprf02p1.func-msp.qa.smf1.mobitv'],
 'msqov-func-msp': [ 'msqov01p1.func-msp.qa.smf1.mobitv',  'msqov02p1.func-msp.qa.smf1.mobitv'],
 'mssch-func-msp': [ 'mssch01p1.func-msp.qa.smf1.mobitv',  'mssch02p1.func-msp.qa.smf1.mobitv'],
 'mssub-func-msp': [ 'mssub01p1.func-msp.qa.smf1.mobitv',  'mssub02p1.func-msp.qa.smf1.mobitv'],
 'msxmp-func-msp': [ 'msxmp01p1.func-msp.qa.smf1.mobitv',  'msxmp02p1.func-msp.qa.smf1.mobitv'],
 'mszoo-func-msp': [ 'mszoo01p1.func-msp.qa.smf1.mobitv',  'mszoo02p1.func-msp.qa.smf1.mobitv',  'mszoo03p1.func-msp.qa.smf1.mobitv'],
 'nocas-func-msp': [ 'nocas01p1.func-msp.qa.smf1.mobitv',  'nocas02p1.func-msp.qa.smf1.mobitv',  'nocas03p1.func-msp.qa.smf1.mobitv'],
 'noslr-old-func-msp': [ 'noslr01p1.func-msp.qa.smf1.mobitv',  'noslr02p1.func-msp.qa.smf1.mobitv'],
 'noslr-new-func-msp': [ 'noslr03p1.func-msp.qa.smf1.mobitv', 'noslr04p1.func-msp.qa.smf1.mobitv','noslr05p1.func-msp.qa.smf1.mobitv'],
 'sqdtb-old-func-msp': [ 'sqdtb01p1.func-msp.qa.smf1.mobitv',  'sqdtb02p1.func-msp.qa.smf1.mobitv'],
 'sqdtb-new-func-msp': [ 'sqdtb03p1.func-msp.qa.smf1.mobitv',  'sqdtb04p1.func-msp.qa.smf1.mobitv'],
 'stdps-func-msp': [ 'stdps01p1.func-msp.qa.smf1.mobitv',  'stdps02p1.func-msp.qa.smf1.mobitv','stdps01p2.func-msp.qa.smf1.mobitv',  'stdps02p2.func-msp.qa.smf1.mobitv'],
 'stmxl-func-msp': [ 'stmxl01p1.func-msp.qa.smf1.mobitv',  'stmxl02p1.func-msp.qa.smf1.mobitv'],
 'stmxv-func-msp': [ 'stmxv01p1.func-msp.qa.smf1.mobitv',  'stmxv02p1.func-msp.qa.smf1.mobitv'],
 'stsgl-func-msp': [ 'stsgl01p1.func-msp.qa.smf1.mobitv',  'stsgl02p1.func-msp.qa.smf1.mobitv'],
 'stval-func-msp': [ 'stval01p1.func-msp.qa.smf1.mobitv',  'stval02p1.func-msp.qa.smf1.mobitv'],
 'stvav-func-msp': [ 'stvav01p1.func-msp.qa.smf1.mobitv',  'stvav02p1.func-msp.qa.smf1.mobitv'],
 'svcar-func-msp': ['svcar01p1.func-msp.qa.smf1.mobitv',   'svcar02p1.func-msp.qa.smf1.mobitv'],
 'svdtm-func-msp': ['svdtm01p1.func-msp.qa.smf1.mobitv',   'svdtm02p1.func-msp.qa.smf1.mobitv'],
 'svftp-func-msp': ['svftp01p1.func-msp.qa.smf1.mobitv',   'svftp02p1.func-msp.qa.smf1.mobitv'],
 'svmgt-func-msp': [ 'svmgt01p1.func-msp.qa.smf1.mobitv'],
    ### PPD-CP
 'juamq-cp-ppd': ['juamq01p1.ppd-cp.devops.smf1.mobitv', 'juamq02p1.ppd-cp.devops.smf1.mobitv'],
 'juarn-cp-ppd': ['juarn01p1.ppd-cp.devops.smf1.mobitv', 'juamq02p1.ppd-cp.devops.smf1.mobitv'],
 'judrm-cp-ppd': ['judrm01p1.ppd-cp.devops.smf1.mobitv', 'judrm02p1.ppd-cp.devops.smf1.mobitv'],
 'juing-cp-ppd': ['juing01p1.ppd-cp.devops.smf1.mobitv', 'juing02p1.ppd-cp.devops.smf1.mobitv'],
 'jujui-cp-ppd': ['jujui01p1.ppd-cp.devops.smf1.mobitv', 'jujui02p1.ppd-cp.devops.smf1.mobitv'],
 'jusch-cp-ppd': ['jusch01p1.ppd-cp.devops.smf1.mobitv', 'jusch02p1.ppd-cp.devops.smf1.mobitv'],
 'juslr-cp-ppd': ['juslr01p1.ppd-cp.devops.smf1.mobitv', 'juslr02p1.ppd-cp.devops.smf1.mobitv'],
 'msamq-cp-ppd': ['msamq01p1.ppd-cp.devops.smf1.mobitv', 'msamq02p1.ppd-cp.devops.smf1.mobitv'],
 'msath-cp-ppd': ['msath01p1.ppd-cp.devops.smf1.mobitv', 'msath02p1.ppd-cp.devops.smf1.mobitv'],
 'msepg-cp-ppd': ['msepg01p1.ppd-cp.devops.smf1.mobitv', 'msepg02p1.ppd-cp.devops.smf1.mobitv'],
 'msfrn-cp-ppd': ['msfrn01p1.ppd-cp.devops.smf1.mobitv', 'msfrn02p1.ppd-cp.devops.smf1.mobitv'],
 'msing-cp-ppd': ['msing01p1.ppd-cp.devops.smf1.mobitv', 'msing02p1.ppd-cp.devops.smf1.mobitv'],
 'msliv-cp-ppd': ['msliv01p1.ppd-cp.devops.smf1.mobitv', 'msliv02p1.ppd-cp.devops.smf1.mobitv'],
 'msnom-cp-ppd': ['msnom01p1.ppd-cp.devops.smf1.mobitv', 'msnom02p1.ppd-cp.devops.smf1.mobitv'],
 'msofm-cp-ppd': ['msofm01p1.ppd-cp.devops.smf1.mobitv', 'msofm02p1.ppd-cp.devops.smf1.mobitv'],
 'msprf-cp-ppd': ['msprf01p1.ppd-cp.devops.smf1.mobitv', 'msprf02p1.ppd-cp.devops.smf1.mobitv'],
 'msqov-cp-ppd': ['msqov01p1.ppd-cp.devops.smf1.mobitv', 'msqov02p1.ppd-cp.devops.smf1.mobitv'],
 'mssch-cp-ppd': ['mssch01p1.ppd-cp.devops.smf1.mobitv', 'mssch02p1.ppd-cp.devops.smf1.mobitv'],
 'mssub-cp-ppd': ['mssub01p1.ppd-cp.devops.smf1.mobitv', 'mssub02p1.ppd-cp.devops.smf1.mobitv'],
 'msxmp-cp-ppd': ['msxmp01p1.ppd-cp.devops.smf1.mobitv', 'msxmp02p1.ppd-cp.devops.smf1.mobitv'],
 'nocas-cp-ppd': ['nocas01p1.ppd-cp.devops.smf1.mobitv', 'nocas02p1.ppd-cp.devops.smf1.mobitv',
                  'nocas03p1.ppd-cp.devops.smf1.mobitv', 'nocas04p1.ppd-cp.devops.smf1.mobitv'],
 'nvrcd-cp-ppd': ['nvrcd01p1.ppd-cp.devops.smf1.mobitv'],
 'nvrcw-cp-ppd': ['nvrcw01p1.ppd-cp.devops.smf1.mobitv'],
 #integration-msp
 'dbmgt-integration-msp': ['dbmgt01p1.integration-msp.smf1.mobitv'],
 'ingan-integration-msp': ['ingan01p1.integration-msp.smf1.mobitv'],
 'inicg-integration-msp': ['inicg01p1.integration-msp.smf1.mobitv'],
 'inldp-integration-msp': ['inldp01p1.integration-msp.smf1.mobitv', 'inldp02p1.integration-msp.smf1.mobitv'],
 'juamq-integration-msp': ['juamq01p1.integration-msp.smf1.mobitv', 'juamq02p1.integration-msp.smf1.mobitv'],
 'juarn-integration-msp': ['juarn01p1.integration-msp.smf1.mobitv', 'juarn02p1.integration-msp.smf1.mobitv'],
 'judrm-integration-msp': ['judrm01p1.integration-msp.smf1.mobitv', 'judrm02p1.integration-msp.smf1.mobitv'],
 'juing-integration-msp': ['juing01p1.integration-msp.smf1.mobitv', 'juing02p1.integration-msp.smf1.mobitv'],
 'jupkg-integration-msp': ['jupkg01p1.integration-msp.smf1.mobitv', 'jupkg02p1.integration-msp.smf1.mobitv'],
 'msamq-integration-msp': ['msamq01p1.integration-msp.smf1.mobitv', 'msamq02p1.integration-msp.smf1.mobitv'],
 'msath-integration-msp': ['msath01p1.integration-msp.smf1.mobitv', 'msath02p1.integration-msp.smf1.mobitv'],
 'msepg-integration-msp': ['msepg01p1.integration-msp.smf1.mobitv', 'msepg02p1.integration-msp.smf1.mobitv'],
 'msfrn-integration-msp': ['msfrn01p1.integration-msp.smf1.mobitv', 'msfrn02p1.integration-msp.smf1.mobitv'],
 'msliv-integration-msp': ['msliv01p1.integration-msp.smf1.mobitv', 'msliv02p1.integration-msp.smf1.mobitv'],
 'msnom-integration-msp': ['msnom01p1.integration-msp.smf1.mobitv', 'msnom02p1.integration-msp.smf1.mobitv'],
 'msofm-integration-msp': ['msofm01p1.integration-msp.smf1.mobitv', 'msofm02p1.integration-msp.smf1.mobitv'],
 'msprf-integration-msp': ['msprf01p1.integration-msp.smf1.mobitv', 'msprf02p1.integration-msp.smf1.mobitv'],
 'msqov-integration-msp': ['msqov01p1.integration-msp.smf1.mobitv'],
 'mssch-integration-msp': ['mssch01p1.integration-msp.smf1.mobitv', 'mssch02p1.integration-msp.smf1.mobitv'],
 'mssub-integration-msp': ['mssub01p1.integration-msp.smf1.mobitv', 'mssub02p1.integration-msp.smf1.mobitv'],
 'msxmp-integration-msp': ['msxmp01p1.integration-msp.smf1.mobitv', 'msxmp02p1.integration-msp.smf1.mobitv'],
 'mszoo-integration-msp': ['mszoo01p1.integration-msp.smf1.mobitv', 'mszoo02p1.integration-msp.smf1.mobitv',
                           'mszoo03p1.integration-msp.smf1.mobitv'],
 'nocas-integration-msp': ['nocas01p1.integration-msp.smf1.mobitv', 'nocas02p1.integration-msp.smf1.mobitv',
                           'nocas03p1.integration-msp.smf1.mobitv'],
 'noslr-integration-msp': ['noslr01p1.integration-msp.smf1.mobitv', 'noslr02p1.integration-msp.smf1.mobitv',
                               'noslr03p1.integration-msp.smf1.mobitv'],
 'sqdtb-integration-msp': ['sqdtb01p1.integration-msp.smf1.mobitv', 'sqdtb02p1.integration-msp.smf1.mobitv'],
 'stdps-integration-msp': ['stdps01p1.integration-msp.smf1.mobitv', 'stdps01p2.integration-msp.smf1.mobitv',
                           'stdps02p1.integration-msp.smf1.mobitv', 'stdps02p2.integration-msp.smf1.mobitv'],
 'stmxl-integration-msp': ['stmxl01p1.integration-msp.smf1.mobitv', 'stmxl02p1.integration-msp.smf1.mobitv',
                           'stmxl03p1.integration-msp.smf1.mobitv', 'stmxl04p1.integration-msp.smf1.mobitv',
                           'stmxl05p1.integration-msp.smf1.mobitv', 'stmxl06p1.integration-msp.smf1.mobitv'],
 'stmxv-integration-msp': ['stmxv01p1.integration-msp.smf1.mobitv', 'stmxv02p1.integration-msp.smf1.mobitv'],
 'stval-integration-msp': ['stval01p1.integration-msp.smf1.mobitv', 'stval02p1.integration-msp.smf1.mobitv'],
 'stvav-integration-msp': ['stvav01p1.integration-msp.smf1.mobitv', 'stvav02p1.integration-msp.smf1.mobitv'],
 'svcar-integration-msp': ['svcar01p1.integration-msp.smf1.mobitv', 'svcar02p1.integration-msp.smf1.mobitv'],
 'svdtm-integration-msp': ['svdtm01p1.integration-msp.smf1.mobitv', 'svdtm02p1.integration-msp.smf1.mobitv'],
 'svftp-integration-msp': ['svftp01p1.integration-msp.smf1.mobitv', 'svftp02p1.integration-msp.smf1.mobitv'],
 'svmgt-integration-msp': [ 'svmgt01p1.integration-msp.smf1.mobitv'],
 #Vmware
 'vmware-prod-msp': ['10.173.97.101', '10.173.97.102',
                        '10.173.97.103', '10.173.97.104',
                        '10.173.97.105', '10.173.97.106',
                        '10.173.97.107', '10.173.97.108',
                        '10.173.97.109', '10.173.97.110',
                        '10.173.97.111', '10.173.97.112',
                        '10.173.97.113'],

}

### Query Puppetdb to dynamically set hosts

enviroment_platform = ""
environment_config = ""
environment_host = ""
environment_ssl_key = ""
environment_ssl_cert = ""
domain = ""
node_facts = []
domain_facts = []
server_list = []
set_hosts = []
magic_all = [ "_all_" ]

def puppetdb_init(platform):
    """
    connect to puppetdb and get data for platform
    """
    global environment_host
    global environment_port
    global environment_ssl_key
    global environment_ssl_cert
    global domain
    global node_facts
    global domain_facts

    enviroment_platform = platform
    environment_config = loadconfig('platform')
    environment_host = environment_config.get(enviroment_platform, 'host')
    environment_port = environment_config.get(enviroment_platform, 'port')
    environment_ssl_key = environment_config.get(enviroment_platform, 'ssl_key')
    environment_ssl_cert = environment_config.get(enviroment_platform, 'ssl_cert')
    domain = environment_config.get(enviroment_platform, 'domain')
    #Connect to puppetdb
    pdb = _puppetdb_connect()
    node_facts = list(pdb.facts('node_type'))
    domain_facts = list(pdb.facts('domain'))

@task(alias='setnode')
def set_env_puppetdb(platform, node_types):
    '''
    fab set_env_puppetdb:'ppd-msp','svcar&svftp'
    '''
    puppetdb_init(platform)
    if node_types in magic_all:
        node_types = _puppetdb_node_types()
    else:
        if '&' in node_types:
            node_types = node_types.split('&')
        else:
            node_types = node_types.split()

    #### Query Puppetdb
    query_puppetdb_nodes(node_types)
    query_puppetdb_domain()
    #print(set_hosts)
    ### Set environment hosts
    env.hosts = set_hosts

def _puppetdb_connect():
    return connect(host=environment_host,
                   ssl_verify=False,
                   port=environment_port,
                   api_version=2,
                   ssl_key=environment_ssl_key,
                   ssl_cert=environment_ssl_cert)

def query_puppetdb_nodes(node_types):
    for node_fact in node_facts:
        if node_fact.value in node_types:
            server_list.append(node_fact.node)

def query_puppetdb_domain():
    for domain_fact in domain_facts:
        if domain_fact.node in server_list and domain_fact.value == domain:
            set_hosts.append(domain_fact.node)


def _puppetdb_node_types():
    """
    return set of node types
    """
    return set(x.value for x in node_facts)

@task(alias='getnode')
def get_env_puppetdb_node_types(platform):
    """
    get the puppetdb facts for a platform
    """
    puppetdb_init(platform)
    print "=== node types ==="
    for node_type in sorted(_puppetdb_node_types()):
        print node_type
@task()
def set_hosts_from_file(argument=None):
    if argument:
        try:
            f = open(argument)
            hosts = f.readlines()
            hosts = [x.strip() for x in hosts]
            env.hosts = hosts
        except IOError:
            print "%s does not exist"%argument
            return
    else:
        sys.exit('No arguments entered')
