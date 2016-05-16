''''' 
Created on 2013-6-2 
 
@author: spch2008 
'''  
  
from wsgiref.simple_server import make_server
import os
import webob
from paste.deploy import loadapp
import sys


class ShowVersion(object):
    def __init__(self, version):
        self.version = version

    def __call__(self, environ, start_response):
        res = webob.Response("version: %s" % self.version)
        res.status = '200 OK'
        return res(environ, start_response)

    @classmethod
    def factory(cls, global_conf, **kwargs):
        print 'ShowVersion'
        return ShowVersion(kwargs['version'])


class LogFilter(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        print 'you can write your log'
        return self.app(environ, start_response)

    @classmethod
    def factory(cls, global_conf, **kwargs):
        print 'LogFilter'
        return LogFilter


if __name__ == "__main__":
    path = os.path.abspath('.') + '/'
    config_name = 'config.ini'
    config_path = path + config_name
    sys.path.append(path)
    app = loadapp('config:%s' % config_path, name='common')
    server = make_server('localhost', 9000, app)
    server.serve_forever()
