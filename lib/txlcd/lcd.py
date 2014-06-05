
class MockLcd(object):
    # buttons
    SELECT                  = 0
    RIGHT                   = 1
    DOWN                    = 2
    UP                      = 3
    LEFT                    = 4

    # colors
    OFF                     = 0x00
    RED                     = 0x01
    GREEN                   = 0x02
    BLUE                    = 0x04
    YELLOW                  = RED + GREEN
    TEAL                    = GREEN + BLUE
    VIOLET                  = RED + BLUE
    WHITE                   = RED + GREEN + BLUE
    ON                      = RED + GREEN + BLUE
    def __init__(self, logger=None):
        self.logger = logger
        self.button = None
        self.text = None
        self.color = None

    def buttonPressed(self, button):
        return button == self.button

    def message(self, text):
        self.text = text
        self.logger.info('lcd text: %s' % text)

    def clear(self):
        self.text = None

    def backlight(self, color):
        if self.color != color:
            self.color = color
            self.logger.info('lcd backlight: %s' % color)
        else:
            pass



