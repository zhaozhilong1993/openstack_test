import logging

from cliff.command import Command

class Simple(Command):
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('sending greeting')
        self.log.debug('debugging')
        self.log.stdout('hello world!\n')