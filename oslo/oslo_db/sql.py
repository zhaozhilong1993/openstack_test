#!/usr/bin/env python
# encoding=utf-8
'''
heat的db模块主要是通过heat-manager对db进行创建，管理的。
所有的与数据库有关的改动都会在heat.db.sqlalchemy.versions下存在
#heat-manager db-sync 这个命令就是用来创建数据库的

margration.py/db_sync函数最后调用的还是oslo_migration这个库

这个文件的部分内容
INIT_VERSION = 27 # 这个是migrate_repo下面的文件编号，没有27的，所以不需要作任何upgrade动作


def db_sync(engine, version=None):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        'migrate_repo')
    return oslo_migration.db_sync(engine, path, version,
                                  init_version=INIT_VERSION)
'''

from oslo_config import cfg
import sys

import sqlalchemy as sql
from oslo_db.sqlalchemy import session as db_session


# 声明配置选项
opts = [
    cfg.StrOpt(
        'connection',
        default='mysql://root:stack@localhost/test?charset=utf-8'
    )
]

opts_group = cfg.OptGroup(
    name='database'
)

CONF = cfg.CONF
# 注册配置项
CONF.register_group(opts_group)
CONF.register_opts(opts, opts_group)
# 声明配置文件
CONF(default_config_files=['sql.conf'])

# 确认OK
print CONF.database.connection

# 开始连接mysql
_facade = None
def get_facade():
    global _facade
    if not _facade:
        _facade = db_session.EngineFacade.from_config(CONF)

def get_engine():
    return get_facade().get_engine()

def get_session():
    return get_facade().get_session()

from oslo_db.sqlalchemy import migration
import sys
import os

engine = sql.create_engine(
    CONF.database.connection,
    echo=True
)

def db_sync():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        'migrate_repo')
    return migration.db_sync(
        engine=engine,
        abs_path=path,
        version=None,
        init_version=27
        )












