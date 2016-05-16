#!/usr/bin/env python



class V1Controller(object):
    def __init__(self):
        self.sub_controllers = {
            "search": SearchController(),
        }
        for name, ctrl in self.sub_controllers.items():
            setattr(self, name, ctrl)


class SearchController(object):
    def __init__(self):
        self.name = 'Search'
        print 'init'

    def post(self):
        print 'post'


a = V1Controller()
print a.search.name