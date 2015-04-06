# coding: utf-8
import json
import logging
import os
import urlparse
import argparse
import codecs

import thriftpy
from thriftpy.rpc import make_server

from ratchet.controller import Ratchet
from ratchet import utils

logger = logging.getLogger(__name__)

__verion__ = 0.1

ratchet_thrift = thriftpy.load(
    os.path.join(os.path.dirname(__file__))+'/ratchet.thrift')

config = utils.Configuration.from_env()
settings = dict(config.items())

ADDRESS = '127.0.0.1'
PORT = '11630'


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

    confs['mongo_uri'] = config.get('app:main', 'mongo_uri')

    return confs


def main():

    parser = argparse.ArgumentParser(
        description="Ratchet Thrift Server"
    )

    parser.add_argument(
        '--address',
         '-a',
        default=ADDRESS,
        help='Binding address (%s)' % ADDRESS
    )

    parser.add_argument(
        '--port',
        '-p',
        default=PORT,
        help='Binding port (%s)' % PORT
    )

    args = parser.parse_args()

    ratchet_controller = Ratchet(settings['app:main']['mongo_uri'])

    dispatcher = Dispatcher(ratchet_controller)

    server = make_server(ratchet_thrift.RatchetStats, dispatcher, args.address, args.port)

    logger.info('Starting Thrift RPC Server at %s:%s.' % (args.address, args.port))

    server.serve()
