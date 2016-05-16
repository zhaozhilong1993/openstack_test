#!/usr/bin/env python
# encoding=utf-8
'''
contextlib.contextmanager装饰器提供了一个上下文的管理器,
但是你还是需要指定上下文，使用yield：
如下面:
   yield 前面的部分就相当于 __enter__
   yield 后面就相当于 __exit__
'''
import contextlib

@contextlib.contextmanager
def test():
    print 'perpare test'
    yield
    print 'after test'


with test():
    print 'hello world'

# 像heat里面的代码
class HeatClient():

    @contextlib.contextmanager
    def _action_recorder(self, action, expected_exceptions=tuple()):
        """Return a context manager to record the progress of an action.

        Upon entering the context manager, the state is set to IN_PROGRESS.
        Upon exiting, the state will be set to COMPLETE if no exception was
        raised, or FAILED otherwise. Non-exit exceptions will be translated
        to ResourceFailure exceptions.

        Expected exceptions are re-raised, with the Resource left in the
        IN_PROGRESS state.
        """
        try:
            self.state_set(action, self.IN_PROGRESS)
            yield
        except expected_exceptions as ex:
            # 中间省略
            pass
        else:
            self.state_set(action, self.COMPLETE)
