#!/usr/bin/env python
# ecoding=utf-8

import mock
import unittest  
from client_patch import multiply
from client_patch import add_and_multiply
  
class MyTestCase(unittest.TestCase):  

    # 传进去的参数可以有很多，但是出来的参数只能是self,也就是被装饰方法的地址
    @mock.patch('client_patch.multiply')
    def test_add_and_multiply(self, mock_multiply):
        print 'log in test_add_and_multiply'

        x = 3  
        y = 5
  
        mock_multiply.return_value = 15  
  
        addition, multiple = add_and_multiply(x, y)  
  
        mock_multiply.assert_called_once_with(3, 5)

        self.assertEqual(8, addition)
        self.assertEqual(15, multiple)
  
if __name__ == "__main__":  
    unittest.main()
