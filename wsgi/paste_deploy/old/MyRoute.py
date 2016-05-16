#!/usr/bin/env python
# encoding=utf-8
"""
__call__方法是对象声明之后可以像函数一样调用它
"""

class a(object):
    def __init__(self, b):
        print '1'

    def __call__(self, x):
        print '3333'


def c():
   d = a(1)
   # 像函数一样
   d
   return d


a(1)