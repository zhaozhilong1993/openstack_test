#!/usr/bin/env python
# ecoding=utf-8

import mock
import testtools
import http
import http_client
import requests
import unittest
from mox3 import mox


class HttpClientTest(unittest.TestCase):

    # Patch os.environ to avoid required auth info.
    def setUp(self):
        super(HttpClientTest, self).setUp()
        self.m = mox.Mox()
        self.m.StubOutWithMock(requests, 'request')
        self.addCleanup(self.m.VerifyAll)
        self.addCleanup(self.m.UnsetStubs)

    def test_http_client_do_something(self):
        headers = {'Content-Type': 'application/octet-stream',
                   'User-Agent': 'python-heatclient'}

        mox.Mox.UnsetStubs(self.m)
        self.m = mox.Mox()
        self.m.StubOutWithMock(requests, 'request')

        # 这个是期望输入 [ 会检测你的期望输入的值是否正确 ]
        mock_conn = requests.request('GET', 'http://example.com:8004',
                                    allow_redirects=False,
                                    headers=headers)

        # 这个是你的期望输出.模拟返回值，假设希望的返回值是200
        expect_return = http.FakeHTTPResponse(status_code=200,
                                              reason='OK',
                                              headers={'content-type': 'application/octet-stream'},
                                              content={})
        mock_conn.AndReturn(expect_return)

        # Replay, create client, assert
        self.m.ReplayAll()
        # 实例化要测试的对象
        client = http_client.HTTPClient('http://example.com:8004')
        # 下面就是你要进行测试的对象的方法了
        resp = client.do_something('GET', 'http://example.com:8004')
        print resp
        # 检测期望输入和输出是否OK
        print expect_return, type(expect_return)
        self.assertEqual(resp, expect_return)


if __name__ == '__main__':
    unittest.main()



