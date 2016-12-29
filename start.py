#!/usr/bin/env python
# coding: utf-8
# yc@2016/12/29
'''
Example
'''

import os
import config
from pyquery import PyQuery as pq
from utils import log, http_get
from simple_threadpool import ThreadPool


def process_block(page):
    log.info('Processing page %d' % page)
    url = 'http://example.com/page/%d' % page
    try:
        d = pq(http_get(url))
        log.info('Got numbers: %s' % d('#cont .date').text())
    except Exception as e:
        log.erro('[ERR] process_block(%d): %s' % (page, e))


def main():
    tp = ThreadPool(config.NUM_THREADS, process_block)
    tp.feed(range(1, 10))
    tp.feed(range(11, 20))
    tp.close()
    log.info('20 pages done')


if __name__ == '__main__':
    main()
    os._exit(0)
