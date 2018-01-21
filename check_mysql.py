#!/usr/local/bin/python2.7
import _mysql
import sys
import argparse

MYSQL_OK = 0
MYSQL_WARNING = 1
MYSQL_CRITICAL = 2
MYSQL_UNKNOWN = 3

globalStatus_thresholds = {

}
processList_thresholds = {
    'dam_user' : (300,300),
    'lm_user' : (100, 100),
    'purchase_user' : (100, 100),
    'acctmgmt_user' : (50, 50),
    'activemq' : (50, 50),
    'ing_user' : (50, 50),
    'mp_user' : (50, 50),
    'wfm_user' : (50, 50),
    'ocsp_user' : (20, 20),
    'pm_user' : (20, 20),
    'netpvr_user' : (20, 20),
    'program_user' : (20, 20),
    'rights_user' : (20, 20),
    'sch_user' : (20, 20),
    'activemq_a' : (20, 20),
    'root' : (5, 5),
    'magento' :  (5, 5),
}

def check_mysql(opts):
    try:
        conn = _mysql.connect(opts.server,
                              opts.user,
                              opts.password,
                              'INFORMATION_SCHEMA')
        conn.query('SELECT USER, count(HOST) FROM INFORMATION_SCHEMA.PROCESSLIST group by USER')
        result = conn.use_result()
        rows = result.fetch_row(0)
        for row in rows:
            user, hostCount = row
            hostCount = int(hostCount)
            if processList_thresholds.has_key(user):
                warning, critical = processList_thresholds[user]
                if hostCount > critical:
                    print 'MySQL CRITICAL: user=%s, actual=%s, threshold=%s' % (user, hostCount, critical)
                    return MYSQL_CRITICAL
                elif hostCount > warning:
                    print 'MySQL WARNING: user=%s, actual=%s, threshold=%s' % (user, hostCount, warning)
                    return MYSQL_WARNING
        #conn.query('SELECT VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_STATUS where VARIABLE_NAME="THREADS_CONNECTED"')
        #conn.query('SELECT VARIABLE_NAME, VARIABLE_VALUE FROM INFORMATION_SCHEMA.GLOBAL_STATUS')
        #result = conn.use_result()
        #rows = result.fetch_row(0)
        #for row in rows:
        #    print row
        print 'MySQL OK'
        return MYSQL_OK
    except Exception as e:
        print 'MySQL unknown error: ' + str(e)
        return MYSQL_UNKNOWN

def parse_cli():
    parser = argparse.ArgumentParser(usage='./check_mysql.py <options>')
    parser.add_argument('-s', '--server', required=True,
                      help='the hostname or ip to the MySQL server')
    parser.add_argument('-u', '--user', required=True,
                        help='user name')
    parser.add_argument('-p', '--password', required=True,
                        help='user password')

    return parser.parse_args()

def main():
    args = parse_cli()
    return check_mysql(args)

if __name__ == '__main__':
    sys.exit(main())
