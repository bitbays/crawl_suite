#!/usr/bin/env python
# coding: utf-8
# yc@2016/12/29

import config
import fabric
from fabric.api import run, env, sudo, parallel, put, cd, prefix
from fabric.context_managers import hide
from fabric.decorators import roles
from fabric.contrib.project import rsync_project

env.use_ssh_config = True
env.colorize_errors = True
env.roledefs = {
    'rpc_nodes': config.RPC_NODES,
}
# https://github.com/fabric/fabric/issues/424
fabric.state.output['running'] = False

RPC_FILE = 'rpc_node.py'
SYNC_EXCLUDES = [
    '.git/', '/logs/', '*.pyc', '*.swp', '.DS_Store', 'fabfile.py', 'config.py'
]


@parallel
@roles('rpc_nodes')
def deploy_rpc():
    '''
    部署 rpc 节点
    '''
    print 'Uploading %s ...' % RPC_FILE
    put(RPC_FILE, '/tmp/')
    pid = _get_rpc_pid()
    if pid:
        print 'Killing previous instance'
        run('kill -9 %s' % pid, warn_only=True)
    print 'Running it...'
    run(
        'nohup python /tmp/%s %s > /tmp/nohup.rpc 2>&1 &'
        % (RPC_FILE, config.RPC_PORT),
        pty=False
    )
    print 'Node deployed: %s' % env.host


def _get_rpc_pid():
    cmd = (
        "ps -Aa -o pid,args | grep %s | grep -v grep | awk '{print $1}'"
        % RPC_FILE
    )
    ret = run(cmd, warn_only=True, shell=False).strip()
    return ret or None


@parallel
@roles('rpc_nodes')
def check_rpc():
    '''
    检查 rpc 节点存活
    '''
    with hide('everything'):
        pid = _get_rpc_pid()
    if pid:
        print '[Alive] %s' % env.host
    else:
        print '[DEAD]  %s' % env.host


def deploy_master():
    '''
    部署主节点
    '''
    if raw_input('Confirm to deploy master on %s?[y/n]' % env.host) != 'y':
        return
    sudo(
        'apt-get update && apt-get install -y python-virtualenv python-pip '
        'libxml2-dev libxslt1-dev python-dev'
    )
    # pip mirror
    run('mkdir -p  ~/.pip', warn_only=True)
    run(
        r'echo -e "[global]\nindex-url = http://pypi.douban.com/simple" > '
        r'~/.pip/pip.conf'
    )
    if run('test -d /data', warn_only=True).failed:
        run('mkdir -p /data/{cs,log,env}')
        run('chmod -R 777 /data')
        run('virtualenv /data/env/cs')
    if run('test -d /data/cs', warn_only=True).failed:
        rsync_project(
            remote_dir='/data/cs', local_dir='./', exclude=SYNC_EXCLUDES
        )
    with cd('/data/cs'), prefix('source /data/env/cs/bin/activate'):
        run('pip install -r requirements.txt')


@parallel
@roles('rpc_nodes')
def tail_rpc():
    '''
    rpc logs
    '''
    run('tail -F /tmp/nohup.rpc', warn_only=True)
