#!/usr/bin/env python
# ecoding=utf-8
'''
oslo_config.cfg主要是用于服务端程序启动的时候需要从配置文件里面读取一些参数而设定的，
如:heat-engine,heat-api等
注册后的参数可以在通过cfg.CONF.<register_group_name>.<cmd>调用

而对于heat这类属于命令行管理工具，通常都是通过子命令实现不同的管理方式
如:heat stack-create其中的stack-create就是subcommand
通常这类程序书写的时候，需要调用heatclient内置的一些函数,实现的方式大多是是getattr()找到对应subcommand
名字的函数执行
'''


from oslo_config import cfg

import socket

opt_group = cfg.OptGroup(
    name='DEFAULT',
    title='default setting'
)
auth_group = cfg.OptGroup(
    name='Auth',
    title='default setting'
)

opts = [
    cfg.StrOpt(
        'host',
        default=socket.gethostname(),
        help='Name of host'
    ),
    cfg.IntOpt(
        'collect_worker',
        default=1,
        help='Number of worker for collector service.'
    ),
    cfg.BoolOpt(
        'roll_back',
        default=False,
        help='roll_back options'
    )
]

CONF = cfg.CONF
# 注册定义好的组
CONF.register_group(opt_group)
# 注册定义好的组
CONF.register_group(auth_group)
# 注册这个组里面的选项,如果你注册了这个组，下面对应的从命令行设置的也要注册到同一个组才会生效
# CONF.register_opts(opts, opt_group)

auth_opts = [
    cfg.StrOpt(
        'auth_url',
        default='http://',
        help='Name of url'
    )
]


# 注册这个组里面的选项
CONF.register_opts(opts)
CONF.register_opts(auth_opts, auth_group)

# 下面将配置选项注册为命令行选项
com_opts = [
    cfg.StrOpt(
        'host',
        default=socket.gethostname(),
        help='Name of host'
    ),
    cfg.IntOpt(
        'collect_worker',
        default=1,
        help='Number of worker for collector service.'
    ),
    cfg.BoolOpt(
        'roll_back',
        default=False,
        help='roll_back options'
    )
]

cfg.CONF.register_cli_opts(com_opts)

# 这样是在/etc下面找service文件夹下面的conf文件
'''
find_config_files(project=None, prog=None, extension='.conf')
    Return a list of default configuration files.

    :param project: an optional project name
    :param prog: the program name, defaulting to the basename of sys.argv[0]
    :param extension: the type of the config file

    We default to two config files: [${project}.conf, ${prog}.conf]

    And we look for those config files in the following directories::

      ~/.${project}/
      ~/
      /etc/${project}/
      /etc/

    We return an absolute path for (at most) one of each the default config
    files, for the topmost directory it exists in.

    For example, if project=foo, prog=bar and /etc/foo/foo.conf, /etc/bar.conf
    and ~/.foo/bar.conf all exist, then we return ['/etc/foo/foo.conf',
    '~/.foo/bar.conf']
'''
default_config_files = cfg.find_config_files('service')

# CONF(default_config_files=default_config_files) #这样是找不到的
# 当前文件夹下的service.conf文件
CONF(default_config_files=['service.conf'])

print CONF.roll_back
print CONF.collect_worker
print CONF.host
print CONF.Auth.auth_url
print cfg.CONF.Auth.auth_url
