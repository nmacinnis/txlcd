import threading

from twisted.internet import reactor, threads


class ButtonMasher(object):
    '''basically just manage the lcd ok??'''
    def __init__(self, logger=None, model=None, lcd=None):
        self.logger = logger
        self.model = model
        self.lcd = lcd

        self.checking = True

        self.message = model.get_latest_message()

        self.lcd_backlight_semaphore = threading.Semaphore()
        self.lcd_time = 0

        if self.message:
            self.logger.debug('buttonmasher initalized with message %s' % self.message.message_text)
        else:
            self.logger.debug('button masher initialized with no message')

    def log_result_and_check_again(self, result):
        if result == self.lcd.SELECT:
            self.logger.debug('\nbutton pressed: select\n')
            self.display_current_message()
        elif result == self.lcd.RIGHT:
            self.logger.debug('\nbutton pressed: right\n')
            pass
        elif result == self.lcd.DOWN:
            self.logger.debug('\nbutton pressed: down\n')
            self.previous_message()
        elif result == self.lcd.UP:
            self.logger.debug('\nbutton pressed: up\n')
            self.next_message()
        elif result == self.lcd.LEFT:
            self.logger.debug('\nbutton pressed: left\n')
            pass

        reactor.callLater(.25, self.start_button_checker)

    def check_buttons(self):
        while self.checking:
            pressed_buttons = filter(
                lambda b: self.lcd.buttonPressed(b),
                range(0, 5)
            )
            if pressed_buttons:
                return pressed_buttons[0]
            threading._sleep(.1)

    def start_button_checker(self):
        d = threads.deferToThread(self.check_buttons)
        d.addCallback(self.log_result_and_check_again)

    def set_lcd_on_time(self, time):
        self.lcd_backlight_semaphore.acquire()
        if time > self.lcd_time:
            self.lcd_time = time
        self.lcd_backlight_semaphore.release()

    def start_screen_lighter(self):
        thread = threading.Thread(target=self.light_lcd_screen)
        thread.start()
        self.logger.info('started screen lighter')
        return thread

    def light_lcd_screen(self):
        while self.checking:
            self.lcd_backlight_semaphore.acquire()
            if self.lcd_time > 0:
                self.lcd_time -= 1
                self.lcd.backlight(self.lcd.TEAL)
            else:
                self.lcd.backlight(self.lcd.OFF)
            self.lcd_backlight_semaphore.release()
            threading._sleep(1)

    def display_current_message(self):
        if not self.message:
            self.logger.debug('nothing to display')
            return
        else:
            self.logger.debug('about to display: %s' % self.message.message_text)
            d = threads.deferToThread(self.display_current_message_in_thread)
            return d

    def display_current_message_in_thread(self):
        message_to_display = self.message
        rows = (len(self.message.message_text) / 16) + 1
        lines = []
        for i in xrange(rows):
            start = i * 16
            end = start + 16
            lines.append(self.message.message_text[start:end])
        if len(lines) == 1:
            lines.append("")
        size = len(lines)
        pairs = zip(lines[0 : size-1], lines[1:size])
        strings = ['\n'.join(p) for p in pairs]

        self.lcd.clear()
        self.set_lcd_on_time(3 + 3 * len(strings))
        for s in strings:
            if self.message != message_to_display:
                return
            self.lcd.clear()
            self.lcd.message(s)
            threading._sleep(3)
        self.lcd.message(strings[0])


    def add_new_message(self, message_text):
        self.message = self.model.add_message(message_text)
        self.display_current_message()

    def next_message(self):
        next_message = self.model.get_next_message(self.message.message_id)
        if next_message:
            self.message = next_message
            self.logger.debug('current message is %s' % self.message.message_text)
        self.display_current_message()

    def previous_message(self):
        previous_message = self.model.get_previous_message(self.message.message_id)
        if previous_message:
            self.message = previous_message
            self.logger.debug('current message is %s' % self.message.message_text)
        self.display_current_message()

    def delete_current_message(self):
        current_message = self.message
        new_message = self.model.get_previous_message(current_message.message_id)
        if not new_message:
            new_message = self.model.get_next_message(current_message.message_id)
        self.model.delete_message(current_message.message_id)
        self.logger.debug('deleted message: %s' % current_message.message_text)
        self.message = new_message
        self.logger.debug('new message is %s' % self.message.message_text)







