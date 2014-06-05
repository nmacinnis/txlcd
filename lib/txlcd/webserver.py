import os

import mako.template
import mako.lookup


class Controller(object):
    def __init__(self, logger=None, button_masher=None):
        self.logger = logger
        self.button_masher = button_masher
        self.template_lookup = mako.lookup.TemplateLookup(directories=[
            os.path.join(os.path.dirname(__file__), 'templates')],
            input_encoding='utf-8', output_encoding='utf-8')

    def render_index(self):
        current_message = self.button_masher.message
        template = self.template_lookup.get_template('lcd.mako')
        response_html = template.render(message=current_message.message_text)
        return response_html

    def get_index(self, request):
        self.logger.debug(request)
        request.write(self.render_index())
        request.finish()

    def get_message(self, request):
        self.logger.debug(request)
        new_message = request.args.get('new_message', [None])[0]
        if new_message:
            self.button_masher.add_new_message(new_message)
        request.write(self.render_index())



