#!/usr/bin/env python
# ecoding=utf-8
import unittest
import mock
import client

class ClientTest(unittest.TestCase):
    def test_success_request(self):
        print 'start test_success_request'
        # 声明mock函数
        success_send = mock.Mock(return_value='200')
        # 假设client的send_request得到的回值就是success_send
        client.send_request = success_send
        # 调用被测试函数
        self.assertAlmostEqual(client.visit_ustack(), '200')

    def test_fail_request(self):
        print 'start test_fail_request'
        faile_send = mock.Mock(return_value='404')
        client.send_request = faile_send
        self.assertAlmostEqual(client.visit_ustack(), '404')

    def test_call_send_request_with_right_arguments(self):
        # 检测调用send_request的时候的参数是str
        client.send_request = mock.Mock()
        client.visit_ustack()
        self.assertEqual(client.send_request.called, True)
        call_args = client.send_request.call_args
        self.assertIsInstance(call_args[0][0], str)



if __name__ == '__main__':
    unittest.main()

