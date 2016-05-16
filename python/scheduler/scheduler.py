#!/usr/bin/env python
# encoding=utf-8

class Test(object):

    def action_handler_task(self, action, args=None, action_prefix=None):
        """A task to call the Resource subclass's handler methods for action.

        Calls the handle_<ACTION>() method for the given action and then calls
        the check_<ACTION>_complete() method with the result in a loop until it
        returns True. If the methods are not provided, the call is omitted.

        Any args provided are passed to the handler.

        If a prefix is supplied, the handler method handle_<PREFIX>_<ACTION>()
        is called instead.
        """
        # 这里部分主要是找到可以执行相应动作的函数
        args = args or []
        handler_action = action.lower()
        check = getattr(self, 'check_%s_complete' % handler_action, None)

        if action_prefix:
            handler_action = '%s_%s' % (action_prefix.lower(), handler_action)
        handler = getattr(self, 'handle_%s' % handler_action, None)

        if callable(handler):
            handler_data = handler(*args)
            # 这里设定一个生成器主要是为了下次再调用这个处理函数的时候可以从这里继续执行
            # 因为保存了上次执行的参数，所以可以检测上次执行的结果
            yield
            # 检测上次的tack是否正确完成,如果没有完成就继续执行，直到完成后退出
            # 这样就可以保证task的正确执行
            if callable(check):
                while not check(handler_data):
                    yield