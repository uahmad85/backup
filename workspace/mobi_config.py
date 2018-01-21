#!/usr/bin/python
import os
import ConfigParser

def loadconfig(module):
    config_store_path = os.path.abspath(os.path.dirname(__file__))
    config_file = os.path.join(config_store_path, '%s.cfg' % module)
    if not os.path.isfile(config_file):
        raise IOError('%s not found' % config_file)

    parser = ConfigParser.SafeConfigParser()
    parser.read(config_file)

    return parser