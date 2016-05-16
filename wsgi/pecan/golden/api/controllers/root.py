from golden.api.controllers.v1 import root as v1
from golden.api.controllers.v2 import root as v2
from golden.api import expose
from pecan import rest
from wsme import types as wtypes


class RootController(rest.RestController):

    v1 = v1.V1Controller()
    v2 = v2.V2Controller()

    @expose.expose(wtypes.text)
    def get(self):
        return 'return value must be text'