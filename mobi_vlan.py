#!/usr/bin/python

from subprocess import Popen,PIPE
import os
nic = None
if os.path.isfile('/etc/sysconfig/network-scripts/ifcfg-eth0'):
    nic = 'eth0'
elif os.path.isfile('/etc/sysconfig/network-scripts/ifcfg-eth1'):
    nic = 'eth1'
else:
    nic = 'eth2'
out = Popen(['ifconfig', nic], stdout=PIPE).communicate()
ips = out[0].split()[6].split(':')[1]
mobi_vlan = ('.').join(ips.split('.')[0:2])
print "%s=%s"%('mobi_vlan',mobi_vlan)
