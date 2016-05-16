#!/usr/bin/env python
# encoding=utf-8
'''
有时候我们在开放程序的时候需要自己建立一个小型的web业务服务器，
如果直接使用apache或者nginx就非常累赘了，所以我们倾向使用自己书写的一个能简单响应web请求的后台程序就好.
但是我们只关心对web请求的处理而不关心对底层http协议的实现（如：解析原始http请求，TCP连接和响应格式之类的）,
这时候我们就需要自己实现一个简单的wsgi程序，python提供了一个wsgiref模块，可以直接使用他建立wsgi站点。

【keystone中利用这个wsgirefs实现了public认证和admin认证的apache插件】
'''

from wsgiref.simple_server import make_server

# 首先我们得先定义一个响应web请求的方法
def application(environ, start_respose):
    header = [(
        'Content-Type',
        'text/html'
    )]
    start_respose('200 ok', header)
    resp = '<h1>Hello World</h1>'
    return resp

# 建立一个wsgi服务器
httpd = make_server('', 9876, application)
print "Server Http on port 9876"

# 开始监听端口
httpd.serve_forever()


