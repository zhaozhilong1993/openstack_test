from golden.api.controllers.v1 import base
from golden.api import expose
from wsme import types as wtypes

"""
class Base(six.with_metaclass(BaseMeta)):
      def __init__(self, **kw):
          for key, value in kw.items():
              if hasattr(self, key):
                  setattr(self, key, value)
"""


class User(wtypes.Base):
    name = wtypes.text
    age = int


class Users(wtypes.Base):
    users = [User]


class UserController(base.BaseController):

    @expose.expose(Users)
    def get(self):
        user_info_list = [{
            'name': 'zhao',
            'age': 23,
        }, {
            'name': 'zhi',
            'age': 23,
        }]
        users_list = [User(**user_info) for user_info in user_info_list]
        return Users(users=users_list)

    # None - this function does get a return value
    # status_code - this function return code status is 201
    # body - client's Http body must follow our defined
    #
    # if you define like expose(None, User, status_code=201)
    # then,your post body should be { "user": {"name": "Cook", "age": 50} }
    #
    #  curl -X POST http://192.168.122.1:8080/v1/user -H "Content-Type: application/json" \
    # -d '{"name": "Cook","age":12}' -v
    @expose.expose(None, body=User, status_code=201)
    def post(self, user):
        print user