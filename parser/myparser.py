#!/usr/bin/env python
# encoding=utf-8
'''
 argparse是命令行程序的一个输入处理函数
 我们知道例如ls和cp等命令都有自己的sumcommand就是子参数,在python中对于这个
 subcommand的定义一般都是使用argparse的工具

 下面的代码思路是根据heatlcient初始化subcommand的代码思路模拟的

 使用方法
 # ./myparser.py list
 会自动调用models/v1/shell.py里面的do_list()方法
'''

import argparse
import sys

'''
class ArgumentParser(_AttributeHolder, _ActionsContainer)
 |  Object for parsing command line strings into Python objects.
 |
 |  Keyword Arguments:
 |      - prog -- The name of the program (default: sys.argv[0])
 |      - usage -- A usage message (default: auto-generated from arguments)
 |      - description -- A description of what the program does
 |      - epilog -- Text following the argument descriptions
 |      - parents -- Parsers whose arguments should be copied into this one
 |      - formatter_class -- HelpFormatter class for printing help messages
 |      - prefix_chars -- Characters that prefix optional arguments
 |      - fromfile_prefix_chars -- Characters that prefix files containing
 |          additional arguments
 |      - argument_default -- The default value for all arguments
 |      - conflict_handler -- String indicating how to handle conflicts
 |      - add_help -- Add a -h/-help option
'''

def get_env_value():
    '''你可以从配置文件中取得参数'''
    return None

def get_base_parser():
    # 初始化你的对象
    parser = argparse.ArgumentParser()
    # 添加你的环境参数
    parser.add_argument("--version",
                        default='1',
                        help='your version'
                        )
    parser.add_argument("--os-token",
                        default=get_env_value(),
                        help='your token'
                        )
    parser.add_argument("--os-password",
                        default=get_env_value(),
                        help='your password'
                        )
    return parser

def import_version_model(version):
    '''利用oslo_utils的库去导入自定义的models'''
    from oslo_utils import importutils
    import sys
    import os
    sys.path.append(os.path.abspath('.'))
    models = 'models.v%s.shell' % version
    return importutils.import_module(models)


def find_action(subparsers, action_models):
    # 你自己定义的运行脚本的名字
    for attr in (a for a in dir(action_models) if a.startswith('do_')):
        # 提取命令名字，需要修改一下
        command = attr[3:].replace('_', '-')
        # 找到函数运行的地址,并运行它
        callback = getattr(action_models, attr)
        desc = callback.__doc__ or ''
        help = desc.strip().split('\n')[0]
        arguments = getattr(callback, 'arguments', [])

        # 添加到parser里面
        subparser = subparsers.add_parser(command,
                                          help=help,
                                          description=desc,
                                          add_help=False
                                          )
        # 设置默认的执行函数
        subparser.set_defaults(func=callback)

def get_subcommand_parser(version):
    # 初始化你的对象
    parser = argparse.ArgumentParser()

    if not version == '1':
        return parser

    # 添加你的基础环境参数
    parser = get_base_parser()
    # 再自定义一些基础参数
    subparser = parser.add_subparsers(metavar='<subcommand>')
    # 倒入对应版本的model
    submodels = import_version_model(version)
    # 加载对应版本里面的model的一些可以执行的命令行参数,加入到subparser中
    find_action(subparser, submodels)

    return parser


class Client():
    def __init__(self, version, endpoint):
        pass


def main(args=None):


    if args is None:
        args = sys.argv[1:]

    # 初始化基础parser环境
    parser = get_base_parser()
    # 提取这个命令的运行环境参数
    (options, argv) = parser.parse_known_args(args)
    # 根据version提取这个命令的subcommand
    subcommand_parser = get_subcommand_parser(options.version)
    # 开始解析输入参数,返回的是一个字典,func里面有对应args的响应函数,[所有的可以执行的model已经在上面导入了]
    # 找到subcommand对应的args信息
    args = subcommand_parser.parse_args(args)
    # 我们可以查看一些刚刚初始化的参数
    #
    #
    # 开始实例化API函数[准备调用api了]
    client = Client(version='1', endpoint='http')
    # 执行args里面的func的函数,入参一个是使用的API，另一个是API带参
    args.func(client, args)

if __name__=='__main__':
    main()



