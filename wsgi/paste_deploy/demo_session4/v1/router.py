''''' 
Created on 2013-6-2 
 
@author: spch2008 
'''  
  
from wsgiref.simple_server import make_server
import os
from paste.deploy import loadapp
import sys
import wsgi

class Controller(object):
    def __init__(self):
        print "Controller"

    def test(self, req):
        print "req",req
        return {
            "name":"test",
            "properties":"test"
        }

class MyRouterApp(wsgi.Router):
    def __init__(self, mapper):
        controller = Controller()
        mapper.connect(
            '/test',
            controller=wsgi.Resource(controller),
            action='test',
            conditions={'method':['GET']}
        )
        super(MyRouterApp, self).__init__(mapper)


if __name__ == "__main__":
    path = os.path.abspath('.') + '/'
    config_name = 'config.ini'
    config_path = path + config_name
    sys.path.append(path)
    app = loadapp('config:%s' % config_path)
    server = make_server('localhost', 9000, app)
    server.serve_forever()
