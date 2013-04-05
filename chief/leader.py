import functools
import logging
import subprocess
import time

from chief import utils

from kazoo.client import KazooClient

LOG = logging.getLogger(__name__)


class ZKFunctionLeader(object):
    def __init__(self, znode_name, hosts, **kwargs):
        if isinstance(hosts, (list, tuple)):
            hosts = ",".join([str(h) for h in hosts])
        self._znode_name = str(znode_name)
        self._client = KazooClient(hosts, **kwargs)
        self._client_started = False

    def start(self, run_what, *args, **kwargs):
        if not self._client_started:
            self._client.start()
            self._client_started = True
        leader_lock = self._client.Lock(self._znode_name)
        LOG.info("Attempting to acquire lock on znode %s on %s",
                 self._znode_name, time.time())
        with leader_lock:
            LOG.info("Acquired lock on znode %s on %s", self._znode_name,
                     time.time())
            try:
                return run_what(*args, **kwargs)
            finally:
                LOG.info("Releasing lock on znode %s on %s", self._znode_name,
                         time.time())


class ZKProcessLeader(ZKFunctionLeader):
    def _run_it(self, binary_name, *args):
        cmd = [str(binary_name)]
        cmd.extend([str(a) for a in args])
        sp = subprocess.Popen(cmd, stdout=None, stderr=None, stdin=None)
        (out, err) = sp.communicate()
        return (out, err, sp.returncode)

    def start(self, binary_name, *args):
        return FunctionLeader.start(self, self._run_it, binary_name, *args)
