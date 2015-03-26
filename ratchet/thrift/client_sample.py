# coding: utf-8
import os
import thriftpy
import json

from thriftpy.rpc import make_client

ratchet_thrift = thriftpy.load(
    os.path.dirname(__file__)+'/ratchet.thrift',
    module_name='ratchet_thrift'
)

if __name__ == "__main__":
    client = make_client(
        ratchet_thrift.RatchetStats,
        '127.0.0.1',
        11631
    )
    print json.loads(client.general('scl'))