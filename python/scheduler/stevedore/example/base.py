import abc


class FormatterBase(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, max_width=60):
        self.max_width = max_width

    @abc.abstractmethod
    def format(self):
        pass