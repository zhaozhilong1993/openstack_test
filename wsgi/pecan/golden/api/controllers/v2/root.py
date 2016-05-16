from golden.api.controllers.v2 import user
from golden.api.controllers.v2 import base
from golden.api import expose
from wsme import types as wtypes


class V2Controller(base.BaseController):

    user = user.UserController()

    @expose.expose(wtypes.text)
    def get(self):
        return 'get'