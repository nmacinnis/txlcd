import random
import threading

from twisted.internet import reactor, threads


class ButtonMasher(object):
    '''basically just manage the lcd ok??'''
    def __init__(self, logger=None, model=None):
        self.logger = logger
        self.model = model

        def log_result_and_check_again(result):
            self.logger.debug(result)
            reactor.callLater(0, self.start_button_checker)

        self.callback = log_result_and_check_again
        self.message = model.get_latest_message()
        if self.message:
            self.logger.debug('buttonmasher initalized with message %s' % self.message.message_text)
        else:
            self.logger.debug('button masher initialized with no message')

    def check_buttons(self):
        while True:
            self.logger.debug("checking buttons")
            for i in xrange(5):
                if random.random() > .95:
                    return True
            threading._sleep(.1)

    def start_button_checker(self):
        d = threads.deferToThread(self.check_buttons)
        d.addCallback(self.callback)






