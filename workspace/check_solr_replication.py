#!/usr/bin/env python
'''
check_solr_replication.py   Hussein Kadiri <hkadiri@mobitv.com>

Nagios check script for checking replication issues on solr slaves.

OPTIONS:

-H : hostname/ip of the solr server we want to query
-p : tcp port solr is listening on
-W : webapp path
-w : delta between master and local replication version, to warn on (default 1)
-c : delta between master and local replication version, to crit on (defualt 2)

EXAMPLE: ./check_solr_replication.py -H localhost -p 8093 -W solr -w 10 -c 20

'''
import requests, json, sys
from optparse import OptionParser

def main():
    global baseurl, core_admin_url, threshold_warn, threshold_crit

    cmd_parser = OptionParser(version="%prog 0.1")
    cmd_parser.add_option("-H", "--host", type="string", action="store", dest="solr_server", default="localhost", help="SOLR Server address")
    cmd_parser.add_option("-p", "--port", type="string", action="store", dest="solr_server_port", default="8080", help="SOLR Server port")
    cmd_parser.add_option("-W", "--webapp", type="string", action="store", dest="solr_server_webapp", default="mobi-solr", help="SOLR Server webapp path")
    cmd_parser.add_option("-w", "--warn", type="string", action="store", dest="threshold_warn", help="WARN threshold for replication check", default=1)
    cmd_parser.add_option("-c", "--critical", type="string", action="store", dest="threshold_crit", help="CRIT threshold for replication check", default=2)

    (cmd_options, cmd_args) = cmd_parser.parse_args()

    if not (cmd_options.solr_server and cmd_options.solr_server_port and cmd_options.solr_server_webapp):
        cmd_parser.print_help()
        return(3)

    if ((cmd_options.threshold_warn and not cmd_options.threshold_crit) or (cmd_options.threshold_crit and not cmd_options.threshold_warn)):
        print "ERROR: Please use -w and -c together."
        return(3)

    if cmd_options.threshold_crit <= cmd_options.threshold_warn:
        print "ERROR: the value for (-c|--critical) must be greater than (-w|--warn)"
        return(3)

    solr_server         = cmd_options.solr_server
    solr_server_port    = cmd_options.solr_server_port
    solr_server_webapp  = cmd_options.solr_server_webapp
    threshold_warn      = cmd_options.threshold_warn
    threshold_crit      = cmd_options.threshold_crit


    try:
      master_resp = requests.get("http://solrmastervip:8080/mobi-solr/replication?command=indexversion&wt=json")
      master_index = master_resp.json()['indexversion']
    except IOError:
      print 'Can not connect to solrmaster solrmastervip'
      return (2)
    try:
      slave_resp = requests.get('http://'+solr_server+':8080/mobi-solr/replication?command=details&wt=json')
      local_index = slave_resp.json()['details']['indexVersion']
    except IOError:
      print 'Can not connect to slave '+solr_server
      return (2)


    index_diff = abs(int(local_index) - int(master_index))
    if index_diff == 0:
      print "OK: slave and master in sync"
      return(0)
    elif index_diff >= int(threshold_warn) and index_diff < int(threshold_warn):
      print "WARNING: differs by "+str(index_diff)
      return(1)
    elif index_diff >= int(threshold_crit):
      print "CRITICAL: index differs by "+str(index_diff)
      return(2)

if __name__ == '__main__':
    sys.exit(main())
    
