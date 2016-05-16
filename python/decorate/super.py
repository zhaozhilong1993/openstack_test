#!/usr/bin/env python
# encoding=utf-8
'''
'''

class demo(object):
    def __init__(self):
        print 'demo'


class demov2(demo):
    def __init__(self):
        print 'demov2'
        super(demov2, self).__init__()

class demov3(demo):
    def __init__(self):
        super(demov3, self).__init__()
        print 'demov3'

# demov2是先实现自己的内部方法再继承demo
# 也就是说demo2先运行了自己的方法，然后再运行了继承类的方法
a = demov2()

# demov3是先继承再实现自己的方法
# 继承的先后和代码的运行顺序有关
b = demov3()
