''''' 
Created on 2013-6-2 
 
@author: spch2008 
'''  
  
from wsgiref.simple_server import make_server
import os
import webob
from paste.deploy import loadapp
import sys


class SayHello(object):
    def __init__(self, version):
        self.version = version

    def __call__(self, environ, start_response):
        res = webob.Response("Hello World!")
        res.status = '200 OK'
        return res(environ, start_response)

    @classmethod
    def factory(cls, global_conf, **kwargs):
        print global_conf
        return SayHello(kwargs['version'])


def app_factory(global_conf, **kwargs):
    print global_conf
    print "app_factory"
    print kwargs
    return SayHello(kwargs['version'])

if __name__ == "__main__":
    path = os.path.abspath('.') + '/'
    config_name = 'config.ini'
    config_path = path + config_name
    sys.path.append(path)
    app = loadapp('config:%s' % config_path)
    server = make_server('localhost', 9000, app)
    server.serve_forever()
