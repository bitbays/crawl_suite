#!/usr/bin/env python
# coding: utf-8
# yc@2015/03/31

import sys
import time
import urllib2
import urllib
import httplib
import random
from SimpleXMLRPCServer import SimpleXMLRPCServer
from socket import error as SocketError

UA = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Ge)'
    'cko) Ubuntu Chromium/33.0.1750.152 Chrome/33.0.1750.152 Safari/537.36'
)
TIMEOUT = 20


def _utf8_dict(obj):
    '''
    fuck urllib.urlencode
    '''
    if type(obj) is str:
        return obj
    ret = {}
    for i, j in obj.items():
        if isinstance(j, unicode):
            ret[i] = j.encode('utf-8')
        else:
            ret[i] = j
    return ret


def _get_req(url, headers=None):
    _headers = {
        'User-Agent': UA,
        'Cache-Control': 'max-age=0',
    }
    if headers:
        _headers.update(headers)
    return urllib2.Request(url, headers=_headers)


def http_post(url, data, headers=None, timeout=TIMEOUT):
    '''
    data: utf-8 encoded dict or json object or str
    '''
    return urllib2.urlopen(
        _get_req(url, headers),
        urllib.urlencode(_utf8_dict(data)),
        timeout=timeout
    ).read()


def http_get(url, headers=None, try_times=1, timeout=TIMEOUT):
    req = _get_req(url, headers)
    for i in range(try_times, 0, -1):
        try:
            return urllib2.urlopen(req, timeout=timeout).read()
        except (urllib2.HTTPError, urllib2.URLError,
                httplib.BadStatusLine, SocketError):
            if i == 1:
                raise
            time.sleep(random.random())


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python %s <port>' % sys.argv[0]
    else:
        port = int(sys.argv[1])
        print 'Running XML-RPC server on port %d' % port
        server = SimpleXMLRPCServer(('0.0.0.0', port), allow_none=True)
        server.register_function(http_post)
        server.register_function(http_get)
        server.serve_forever()
