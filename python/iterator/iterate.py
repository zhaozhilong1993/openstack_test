#!/usr/bin/env python
# encoding = utf-8

# 迭代器
class feb():
    def __init__(self, max):
        self.max = max
        self.a = 0
        self.b = 1
        self.n = self.a

    def __iter__(self):
        return self

    def next(self):
        if self.n < self.max:
            self.n = self.a + self.b
            self.a = self.b
            self.b = self.n
            return self.n

        raise StopIteration


inter = feb(5)

print inter.next()
print inter.next()
print inter.next()
print inter.next()
print inter.next()


