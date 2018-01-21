import argparse

def parse_cli():
    parser = argparse.ArgumentParser(usage='./check_mysql.py <options>')
    parser.add_argument('-s', '--server', required=True,
                      help='the hostname or ip to the MySQL server')
    parser.add_argument('-u', '--user', required=True,
                        help='user name')
    parser.add_argument('-p', '--password', required=True,
                        help='user password')

    return parser.parse_args()
ab = parse_cli()
print ab

