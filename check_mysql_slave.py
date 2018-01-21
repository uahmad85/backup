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
replication_thresholds = {
    'Seconds_Behind_Master' : (1,5),
}

def check_mysql(opts):
    try:
        conn = _mysql.connect(host=opts.server,
                              port=int(opts.port),
                              user=opts.user,
                              passwd=opts.password,
                              db='INFORMATION_SCHEMA')
        conn.query("SHOW SLAVE STATUS")
        result = conn.use_result()
        metrics = map(lambda x: x[0], result.describe())
        values = result.fetch_row(0)[0]
        for metric,value in zip(metrics,values):
            # print metric
            if replication_thresholds.has_key(metric):
                value = int(value)
                warning, critical = replication_thresholds[metric]
                if value > critical:
                    print 'MySQL CRITICAL: metric=%s, actual=%s, threshold=%s' % (metric, value, critical)
                    return MYSQL_CRITICAL
                elif value > warning:
                    print 'MySQL WARNING: metric=%s, actual=%s, threshold=%s' % (metric, value, warning)
                    return MYSQL_WARNING
        print 'MySQL REPLICATION OK'
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
    parser.add_argument('-P', '--port', required=True,
                        help='port')

    return parser.parse_args()

def main():
    args = parse_cli()
    return check_mysql(args)

if __name__ == '__main__':
    sys.exit(main())
