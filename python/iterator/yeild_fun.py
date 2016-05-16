#!/usr/bin/env python
# encoding=utf-8
'''
生成器的定义就是：在循环过程中可以计算出下次迭代的结果，从而实现不断生成下一步的
一个函数，所以生成器可以使用的条件:
  1).根据上次循环的结果推算出下次循环的结果

生成器可以直接由列表生成式生成:
生成列表:
g = [x * x for x in range(10)]
生成生成器:
g = (x * x for x in range(10))

另一种方法就是在函数里面定义:
使用yield方法
'''


# 1). 列表生成式
g = (x * x for x in range(10))

# <type 'generator'>
print type(g)


# 2). 生成器yeild
def feb(max_length):
    # 初始化
    a = 1
    b = 1
    n = 0
    while n < max_length:
        yield (a, b)
        # 生成下次迭代的值
        t = a + b
        # 移动
        a = b
        b = t
        n = n + 1


# for循环访问
for a in feb(10):
    print a

# 直接next访问
c = feb(10)
print c.next()
print c.next()
print c.next()