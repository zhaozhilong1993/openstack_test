# encoding=utf-8
'''''
在
'''  
  
from wsgiref.simple_server import make_server
import os
from paste.deploy import loadapp
import sys
import wsgi
import routes
import webob

class Controller(object):
    def __init__(self):
        print "Controller"

    def __call__(self, *args, **kwargs):
        return 'call'

    def GET(self):
        return "GET"

    def POST(self):
        return "POST"

class MyRouterApp(object):
    def __init__(self, mapper):
        app = Controller()
        mapper = routes.Mapper()
        mapper.connect('/test',controller=app,action='POST',conditions={'method':['POST']})
        self.map = mapper
        self._router = routes.middleware.RoutesMiddleware(self._dispatch,
                                                         self.map)

    @webob.dec.wsgify
    def __call__(self, req):
        """
        Route the incoming request to a controller based on self.map.
        If no match, return a 404.
        """
        return self._router

    @staticmethod
    @webob.dec.wsgify
    def _dispatch(req):
        """
        Called by self._router after matching the incoming request to a route
        and putting the information into req.environ.  Either returns 404
        or the routed WSGI app's response.
        """
        match = req.environ['wsgiorg.routing_args'][1]
        if not match:
            return webob.exc.HTTPNotFound()

        action = match['action']
        controller = match['controller']

        if hasattr(controller, action):
            func = getattr(controller,action)
            ret = func()
            return ret
        else:
            return 'Not has this method'


    @classmethod
    def factory(cls, global_conf, **local_conf):
        return cls(routes.Mapper())




if __name__ == "__main__":
    path = os.path.abspath('.') + '/'
    config_name = 'config.ini'
    config_path = path + config_name
    sys.path.append(path)
    app = loadapp('config:%s' % config_path)
    server = make_server('localhost', 9000, app)
    server.serve_forever()
