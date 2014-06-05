

class Controller(object):
    def __init__(self, logger=None, button_masher=None):
        self.logger = logger
        self.button_masher = button_masher

    def get_index(self, request):
        self.logger.debug(request)
        current_message = self.button_masher.message
        response_html = str('<html>%s</html>' % current_message.message_text)
        self.logger.debug(response_html)
        request.write(response_html)
        request.finish()




