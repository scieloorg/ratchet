# coding: utf-8
import json
import logging
import os
import urlparse
import argparse
import ConfigParser
import codecs

import daemon
import lockfile
import thriftpy
from thriftpy.rpc import make_server
from thriftpy.protocol import TCyBinaryProtocolFactory
from thriftpy.transport import TCyBufferedTransportFactory, TTransportException

from ratchet.controller import Ratchet


logger = logging.getLogger(__name__)

__verion__ = 0.1

LOG_FMT = r"%(asctime)s %(name)s[%(process)d] [%(levelname)s] %(message)s"
BIND_IP = '127.0.0.1'
BIND_PORT = '11630'
PROTOCOL = TCyBinaryProtocolFactory()
TRANSPORT = TCyBufferedTransportFactory()


ratchet_thrift = thriftpy.load(os.path.join(os.path.dirname(__file__))+'/ratchet.thrift')

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

def run_server(host, port, dispatcher):
    u""" 
    Inicia o servidor RPC no host e porta especificados.
    """

    server = make_server(ratchet_thrift.RatchetStats, dispatcher,
                         host, port, proto_factory=PROTOCOL, trans_factory=TRANSPORT)

    logger.info('Starting Thrift RPC Server at %s:%s. Using protocol %s and transport %s.' % (
        host, port, PROTOCOL, TRANSPORT,))

    print("Serving...")

    try:
        server.serve()

    except KeyboardInterrupt:
        print("Shutting down...")

    finally:
        logger.info('Shutting down Thrift RPC Server')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Ratchet Thrift Server"
    )

    parser.add_argument(
        'host',
        nargs='?',
        default=BIND_IP,
        help='bind ip (%s)' % BIND_IP
    )

    parser.add_argument(
        'port',
        nargs='?',
        default=BIND_PORT,
        help='bind port (%s)' % BIND_PORT
    )

    parser.add_argument(
        '--config_file',
        '-c',
        help='Pyramid config file'
    )

    parser.add_argument(
        '--daemon',
        action='store_true'
    )

    parser.add_argument(
        '--pidfile',
        '-p',
        help='Absolute path to the pid file (daemon only)'
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

    logging_opt_conf = {}
    if args.logging_file:
        logging_opt_conf['filename'] = args.logging_file

    if args.daemon:
        daemon_options = {'umask': 0o002}
        if args.pidfile:
            daemon_options['pidfile'] = lockfile.FileLock(args.pidfile)

        context = daemon.DaemonContext(**daemon_options)
        with context:
            logging.basicConfig(format=LOG_FMT,
                level=getattr(logging, args.logging_level), **logging_opt_conf)
            ratchet_controller = Ratchet(confs['mongo_uri'])
            run_server(args.host, args.port, Dispatcher(ratchet_controller))

    else:
        logging.basicConfig(format=LOG_FMT,
            level=getattr(logging, args.logging_level), **logging_opt_conf)
        ratchet_controller = Ratchet(confs['mongo_uri'])
        run_server(args.host, args.port, Dispatcher(ratchet_controller))
