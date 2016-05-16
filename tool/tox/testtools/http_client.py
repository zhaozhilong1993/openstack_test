#!/usr/bin/env python
# ecoding=utf-8

import requests

class HTTPClient(object):

    def __init__(self, url):
        self.url = url

    # 首先，我有一个封装了requests方法的函数
    # 我要和其他系统进行集成，都会调用这个方法去访问其他系统的API
    # 比如heat需要去访问8004端口也就是heat-api的端口
    def request(self, method, url):

        headers = {'Content-Type': 'application/octet-stream',
                   'User-Agent': 'python-heatclient'}

        resp = requests.request(
            method,
            url,
            allow_redirects=False,
            headers=headers
        )

        return resp

    # 这里有一个模拟的动作，具体做什么，我没有定义
    # 类似这样的方法有很多: 获取token, 检验tamplate, 访问数据库
    # 但是所有的这些动作都有一个共同的出口，就是上面的request
    def do_something(self, method, url):
        print 'i can do everything i want!'
        resp = self.request(method, url)
        return resp

    def deal_with(self, content):
        pass

# 如果没有单元测试，你就需要自己去搭建一台keystone服务器进行交互 - 烦
# 或者你自己在代码中预定义好值，之后测试好之后又改回来，但是如果调用的地方很多就会浪费大量的时间 - 效率低
# client = HTTPClient('http://keystone.com:5000')
# client.do_something('GET', 'http://heat-api.com:8004')

