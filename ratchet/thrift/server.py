# coding: utf-8
import json
import logging
import os
import urlparse
import argparse
import ConfigParser
import codecs

import thriftpy
from thriftpy.rpc import make_server

from ratchet.controller import Ratchet


logger = logging.getLogger(__name__)

ratchet_thrift = thriftpy.load(
    os.path.dirname(__file__)+'/ratchet.thrift',
    module_name='ratchet_thrift'
)

BIND_IP = '127.0.0.1'
BIND_PORT = '11631'

def _config_logging(logging_level='INFO', logging_file=None):

    allowed_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger('ratchet_thrift')
    logger.setLevel(allowed_levels.get(logging_level, 'INFO'))

    if logging_file:
        hl = logging.FileHandler(logging_file, mode='a')
    else:
        hl = logging.StreamHandler()

    hl.setFormatter(formatter)
    hl.setLevel(allowed_levels.get(logging_level, 'INFO'))

    logger.addHandler(hl)

    return logger

class Dispatcher(object):

    def __init__(self, ratchet_controller):
        self._ratchet = ratchet_controller

    def general(self, code):

        data = self._ratchet.general(code=code)

        return json.dumps(data)


def loadconfs(config_file):

    confs = {}
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(config_file)

    try:
        confs['mongo_uri'] = config.get('app:main', 'mongo_uri')
    except ConfigParser.NoOptionError:
        confs['mongo_uri'] = 'mongodb://127.0.0.1:27017/ratchet'

    return confs

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Ratchet Thrift server"
    )

    parser.add_argument(
        '--config_file',
        '-c',
        help='Pyramid config file'
    )

    parser.add_argument(
        'bind_ip',
        nargs='?',
        default=BIND_IP,
        help='bind ip (%s)' % BIND_IP
    )

    parser.add_argument(
        'bind_port',
        nargs='?',
        default=BIND_PORT,
        help='bind port (%s)' % BIND_PORT
    )

    parser.add_argument(
        '--pid_file',
        '-p',
        default='/var/run/ratchet_thrift.pid',
        help='pid_file'
    )

    parser.add_argument(
        '--logging_file',
        '-o',
        default='/var/log/ratchet/thrift_server.log',
        help='Full path to the log file'
    )

    parser.add_argument(
        '--logging_level',
        '-l',
        default='DEBUG',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Logggin level'
    )

    args = parser.parse_args()

    confs = loadconfs(open(args.config_file))

    logger = _config_logging(args.logging_level, args.logging_file)

    ratchet_controller = Ratchet(confs['mongo_uri'])

    with open(args.pid_file, 'w') as f:
        f.write(str(os.getpgrp()))

    server = make_server(
        ratchet_thrift.RatchetStats,
        Dispatcher(ratchet_controller),
        args.bind_ip, args.bind_port
    )

    print 'Serving at: %s:%s' % (args.bind_ip, args.bind_port)

    server.serve()
