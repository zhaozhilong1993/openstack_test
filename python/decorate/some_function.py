#!/usr/bin/env python


state = None


def proxy(key):
    class ObjectProxy(object):

        explanation_ = AttributeError(
            "`pecan.state` is not bound to a context-local context.\n"
            "Ensure that you're accessing `pecan.request` or `pecan.response` "
            "from within the context of a WSGI `__call__` and that "
            "`use_context_locals` = True."
        )

        def __getattr__(self, attr):
            print attr
            '''
            try:
                obj = getattr(state, key)
            except AttributeError:
                raise self.explanation_
            return getattr(obj, attr)
            '''

        def __setattr__(self, attr, value):
            obj = getattr(state, key)
            return setattr(obj, attr, value)

        def __delattr__(self, attr):
            obj = getattr(state, key)
            return delattr(obj, attr)

        def __dir__(self):
            obj = getattr(state, key)
            return dir(obj)

    return ObjectProxy()


request = proxy('request')
response = proxy('response')


from ceilometer.api.controllers.v2 import utils
from ceilometer import storage


request.storage_conn.get_samples()
