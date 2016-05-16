''''' 
Created on 2013-6-2 
 
@author: spch2008 
'''  
  
from wsgiref.simple_server import make_server  

import routes.middleware
import webob.dec
import webob.exc
from paste.deploy import loadapp  

class Controller:
    @webob.dec.wsgify
    def __call__(self, req):
        return webob.Response("Hello World!")



class Router(object):
    def __init__(self):
        self._mapper = routes.Mapper()
        self._mapper.connect('/hello',
                        controller=Controller(),
                        action='index',
                        conditions={'method': ['GET']})


        self._router = routes.middleware.RoutesMiddleware(self._dispatch, self._mapper)

    @classmethod
    def app_factory(cls, global_config, **local_config):
        return cls()

    @webob.dec.wsgify
    def __call__(self, req):
        return self._router



    @staticmethod
    @webob.dec.wsgify
    def _dispatch(req):
        match = req.environ['wsgiorg.routing_args'][1]
        import pdb
        pdb.set_trace()

        if not match:
            return webob.exc.HTTPNotFound()

        app = match['controller']
        return app


def factory(**local_conf):
    print (local_conf)
    return Router()


def hello(loader, **local_conf):
    print loader
    print (local_conf)
    return Router()


if __name__ == "__main__":
    app = loadapp('config:/root/Desktop/code/myopenstack/wsgi/paste_deploy/config2.ini')
    httpd = make_server('localhost', 9000, app)
    httpd.serve_forever()