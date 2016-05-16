#!/usr/bin/env python
# encoding=utf-8
import six
import pecan
# 1). 把do_action传入到装饰器wrappertask中
def wrappertask(task):

    @six.wraps(task)
    def wrapper(**kwargs):
        print kwargs
        print 'warpper'
        print task
        task(noAuth = True)

    print 'warppertask'
    return wrapper


def wrappertask2(task):

    @six.wraps(task)
    def wrapper(self, **kwargs):
        global no_auth
        no_auth = False
        print 'in warpper:', self
        print kwargs
        print 'warpper2'
        print task
        task(self, **kwargs)

    print 'warppertask2'
    return wrapper

class test(object):

    @pecan.expose('json')
    @wrappertask2
    def do_action(self, **kwargs):
        if no_auth:
            print 'noAuth'
        else:
            print 'Auth'



a = test()
a.do_action()
