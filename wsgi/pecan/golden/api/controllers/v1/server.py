from golden.api.controllers.v1 import base
from golden.api import expose
from wsme import types as wtypes
import pecan


class Server(wtypes.Base):
    # request post body have key for "id"
    id = wtypes.wsattr(wtypes.text, mandatory=True)
    age = int
    name = wtypes.text


class ServerController(base.BaseController):
    def __init__(self, server_id):
        self.server_id = server_id

    # curl http://192.168.122.1:8080/v1/server/1234
    @expose.expose(Server)
    def get(self):
        server_info = {
            'id': self.server_id,
            'age': 22,
            'name': 'test'
        }
        return Server(**server_info)

    # we also can use post method like
    # curl -X POST http://192.168.122.1:8080/v1/server/1234 -H "Content-Type: application/json" \
    # -d '{"name": "Cook",id:"123"}' -v
    @expose.expose(None, body=Server, status_code=201)
    def post(self, server):
        print server

    # curl -X PUT http://localhost:8080/v1/server/123 -H "Content-Type: application/json" \
    # -d '{"name": "Cook", "id":"123"}'
    @expose.expose(Server, body=Server)
    def put(self):
        server_info = {
            'id': self.server_id,
            'age': 22,
            'name': 'test'
        }
        return Server(**server_info)

    @expose.expose(None)
    def delete(self):
        print 'Delete server_id: %s' % self.server_id

    # curl -X PUT http://localhost:8080/v1/server/123 -H "Content-Type: application/json" \
    # -d '{"name": "Cook", "id":"123"}'
    @expose.expose(Server, body=Server)
    def update(self):
        server_info = {
            'id': self.server_id,
            'age': 22,
            'name': 'update'
        }
        return Server(**server_info)

class ServersController(base.BaseController):

    # notice: this pecan.expose() is not define by me
    # Don't use expose define by ours
    @pecan.expose()
    def _lookup(self, server_id, *remainder):
        return ServerController(server_id), remainder