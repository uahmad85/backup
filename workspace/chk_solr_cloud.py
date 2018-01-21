#!/usr/bin/env python
'''

OPTIONS:
-H hostname/ip
-p port
-U url for cluster status

Example ./chk_solr_cloud.py -H noslr01p1.prod-msp.smf1.mobitv -p 8983

'''
import json
import requests
from optparse import OptionParser
import sys


def main():
    parser = OptionParser()
    parser.add_option("-H","--host", type="string", action="store",dest="solr_cloud_server",help="Solr Cloud fqdn")
    parser.add_option("-p","--port", type="string", action="store", dest="solr_port", default="8983",help=" Port solr cloud is listening on")
    parser.add_option("-U","--url", type="string", action="store", dest="status_url", default="/mobi-solr/admin/collections?action=CLUSTERSTATUS&wt=json", help="Cluster Status url")
    (command_options, command_args) = parser.parse_args()
    if not (command_options.solr_cloud_server):
        parser.print_help()
        return(2)
    solr_cloud_server = command_options.solr_cloud_server
    solr_port = command_options.solr_port
    status_url = command_options.status_url
    check_url = 'http://' + solr_cloud_server + ':' + solr_port + status_url
    short_host = solr_cloud_server.split('.')[0]

    try:
        check_response = requests.get(check_url).json()
    except Exception as error:
        print "NOK {0}".format(error)
        return(2)

    for noslr in check_response.values()[0]["collections"]["mobi-solr-collection"]["shards"]["shard1"]["replicas"]:
        if check_response.values()[0]["collections"]["mobi-solr-collection"]["shards"]["shard1"]["replicas"][noslr]["node_name"].split(":")[0] == short_host:
            if check_response.values()[0]["collections"]["mobi-solr-collection"]["shards"]["shard1"]["replicas"][noslr]["state"] == "active":
                print "OK"
                return(0)
            else:
                print "NOK {0} is down".format(solr_cloud_server) 
                return(2)

if __name__ == '__main__':
    sys.exit(main())
