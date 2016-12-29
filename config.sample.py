#!/usr/bin/env python
# coding: utf-8
# yc@2016/12/29

PROJECT_NAME = 'cs_test'
# RPC 的 HTTP 超时
HTTP_TIMEOUT = 30
# GET 失败总共重试 3 次
HTTP_TRY_TIMES = 3
# 并发
NUM_THREADS = 10
# 日志
DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'
LOG_FILE = '/tmp/crawl_%s.log' % PROJECT_NAME
# 抓取节点, ssh config 里的配置，供 fabfile 部署用
RPC_NODES = [
    'host1', 'host2',
]
RPC_PORT = 59421
# TODO nodes 的 ip 地址列表
RPC_NODE_IPS = []
RPC_NODE_URLS = [
    'http://%s:%s' % (i, RPC_PORT) for i in RPC_NODE_IPS
]
