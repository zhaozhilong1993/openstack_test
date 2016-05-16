#!/usr/bin/env python
# encoding=utf-8
from wsgiref.simple_server import make_server
import os
import webob
from paste.deploy import loadapp
import sys


'''
一般,每一个在paste的配置文件里面被调用的函数都会有factory这个函数，当然你可以自己设定名字，但是factory肯定要返回
这个类
'''
class SayHello(object):
    def __init__(self, version):
        self.version = version

    def __call__(self, environ, start_response):
        res = webob.Response("Hello World!")
        res.status = '200 OK'
        return res(environ, start_response)

    @classmethod
    def factory(cls, global_conf, **kwargs):
        print '1.0'
        return SayHello(kwargs['version'])


if __name__ == "__main__":
    path = os.path.abspath('.') + '/'
    config_name = 'config.ini'
    config_path = path + config_name
    sys.path.append(path)
    app = loadapp('config:%s' % config_path)
    server = make_server('localhost', 9000, app)
    server.serve_forever()
