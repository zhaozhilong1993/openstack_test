from golden.api.controllers.v1 import base
from golden.api.controllers.v1 import user
from golden.api.controllers.v1 import server
from golden.api import expose
from wsme import types as wtypes


class V1Controller(base.BaseController):

    user = user.UserController()
    server = server.ServersController()

    @expose.expose(wtypes.text)
    def get(self):
        return 'get'