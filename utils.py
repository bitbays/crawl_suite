#!/usr/bin/env python
# coding: utf-8
# yc@2016/02/16

import logging
import logging.handlers
import datetime
import httplib
import config
import xmlrpclib
from itertools import cycle


__all__ = ['log', 'now', 'now_py', 'http_get']


now_py = datetime.datetime.now
now = lambda: now_py().strftime(config.DATETIME_FORMAT)
log = logging.getLogger(config.PROJECT_NAME)
rpc_nodes = cycle(config.RPC_NODE_URLS)


class TransportWithTimeout(xmlrpclib.Transport):
    '''
    带超时设置的 Transport
    '''
    def make_connection(self, host):
        if self._connection and host == self._connection[0]:
            return self._connection[1]
        chost, self._extra_headers, x509 = self.get_host_info(host)
        self._connection = host, httplib.HTTPConnection(
            chost, timeout=config.HTTP_TIMEOUT)
        return self._connection[1]


def http_get(url, try_times=3, timeout=None):
    uri = rpc_nodes.next()
    rpc = xmlrpclib.ServerProxy(
        uri, allow_none=True, transport=TransportWithTimeout()
    )
    return rpc.http_get(url, {}, try_times, timeout or config.HTTP_TIMEOUT)


def init_logger(out_file=None):
    if out_file:
        # file
        handler = logging.handlers.RotatingFileHandler(
            out_file,
            # 50MB
            maxBytes=1024*1024*50,
            backupCount=5
        )
    else:
        # stderr
        handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('[%(asctime)s]-%(levelname)s: %(message)s')
    )
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)


# init logger
init_logger(config.LOG_FILE)
