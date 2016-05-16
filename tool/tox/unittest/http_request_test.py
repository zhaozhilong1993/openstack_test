#!/usr/bin/env python
# ecoding=utf-8

import mock
from mox3 import mox
import testtools
import http
import http_client
import requests
import unittest



class HTTPClientTest(unittest.TestCase):
    def test_http_client_do_something(self):
        headers = {'Content-Type': 'application/octet-stream',
                   'User-Agent': 'python-heatclient'}

        # Record a 200
        requests.request = mock.Mock(return_value={
            'headers': headers,
            'status_code': 200,
            'content': 100,
        })

        # 实例化要测试的对象
        client = http_client.HTTPClient('http://example.com:8004')
        # 下面就是你要进性测试的对象的方法了
        resp = client.do_something('GET', '')
        # 这就是你期望给的回值，有了这些回值之后程序是否可以正常运行
        self.assertEqual(200, resp['status_code'])

if __name__ == '__main__':
    unittest.main()



