
#!/usr/bin/env python
# encoding=utf-8
'''
mock模块是提供单元测试的模块,主要就是用mock函数替换掉你向测试的函数
这个文件是模拟了开放环境里的运行环境，如：
  你写好了一个API函数，但是你想去其他系统上调用其他的API函数，如果花时间再去搭建一个测试
  系统，那就太浪费时间了。
  所以，可以使用mock模块模拟其他系统上的API的回值，我们设置一个期望得到的值，然后除理他就好

测试函数和测试代码必须和生产代码分开，这是毋庸置疑的，所以测试代码在test目录下
'''
import requests

def send_request(url):
    r = requests.get(url)
    return r.status_code

def visit_ustack():
    http_status = send_request('http://213www.ustack.com')

    if http_status:
        print 'good'
    else:
        print 'false'
    return http_status

# 直接访问OK
# print visit_ustack()

