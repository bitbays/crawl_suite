# Crawl Suite
Tools for crawling and parsing web pages


## Components included
+ `simple_threadpool` for thread pool
+ `fabric` for deployment
+ `pyquery` for querying DOM
+ `xmlrpclib` for clustering


## Customize
+ `cp config.sample.py config.py`
+ Edit `config.py`, add rpc nodes


## Usage
```shell
# deploy rpc nodes
fab deploy_rpc
# check rpc nodes (when Dead, bring it back with deploy_rpc)
fab check_rpc
# check rpc logs
fab tail_rpc
# deploy master node
fab -H host1 deploy_master
```
