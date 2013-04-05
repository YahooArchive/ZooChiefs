#!/usr/bin/env python

import argparse
import hashlib
import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.abspath(os.pardir)))
sys.path.insert(0, os.path.abspath(os.getcwd()))

from chief import leader

ZNODE_TPL = '/pc-%s'


def setup_logging(log_level, format='%(process)d %(levelname)s: @%(name)s : %(message)s'):
    root_logger = logging.getLogger()
    console_logger = logging.StreamHandler(sys.stdout)
    console_logger.setFormatter(logging.Formatter(format))
    root_logger.addHandler(console_logger)
    root_logger.setLevel(log_level)


def _get_znode(bin):
    m = hashlib.new('md5')
    m.update(str(bin))
    return ZNODE_TPL % (m.hexdigest())


def run_solo():
    parser = argparse.ArgumentParser()
    parser.add_argument('binary', metavar='binary', type=str, nargs=1,
                        help='main program')
    parser.add_argument('args', metavar='arg', type=str, nargs='*',
                        help='program arguments')
    parser.add_argument('--zk-server', '-z', action='append',
                        help='zookeeper server address',
                        default=['localhost:2181'])
    parser.add_argument('--verbose', '-v', action='append_const', const=1,
                        help='increase verbosity')
    args = parser.parse_args()
    if not args.binary:
        parser.error("No binary provided")
    if len(args.verbose) >= 2:
        setup_logging(logging.DEBUG)
    elif len(args.verbose) == 1:
        setup_logging(logging.INFO)
    else:
        setup_logging(logging.ERROR)
    znode_name = _get_znode(args.binary[0])
    c = leader.ZKProcessLeader(znode_name, args.zk_server)
    (_out, _err, rc) = c.start(args.binary[0], *args.args)
    return rc


if __name__ == '__main__':
    sys.exit(run_solo())
