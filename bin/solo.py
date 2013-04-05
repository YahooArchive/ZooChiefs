#!/usr/bin/env python

import argparse
import os
import logging
import sys

sys.path.insert(0, os.path.join(os.path.abspath(os.pardir)))
sys.path.insert(0, os.path.abspath(os.getcwd()))

from chief import leader


def setup_logging(log_level, format='%(process)d %(levelname)s: @%(name)s : %(message)s'):
    root_logger = logging.getLogger()
    console_logger = logging.StreamHandler(sys.stdout)
    console_logger.setFormatter(logging.Formatter(format))
    root_logger.addHandler(console_logger)
    root_logger.setLevel(log_level)


def run_solo():
    parser = argparse.ArgumentParser()
    parser.add_argument('binary', metavar='binary', type=str, nargs=1,
                        help='main program')
    parser.add_argument('args', metavar='arg', type=str, nargs='*',
                        help='program arguments')
    parser.add_argument('--zk-server', '-z', action='append',
                        help='zookeeper server address',
                        default=['localhost:2181'])
    parser.add_argument('--verbose', '-v', action='store_true', default=False,
                        help='increase verbosity')
    args = parser.parse_args()
    if not args.binary:
        parser.error("No binary provided")
    if args.verbose:
        setup_logging(logging.DEBUG)
    else:
        setup_logging(logging.INFO)
    znode_name = '/proc-leader-%s' % (args.binary)
    c = leader.ZKProcessLeader(znode_name, args.zk_server)
    return z.start(args.binary, *args.args)


if __name__ == '__main__':
    sys.exit(run_solo())
