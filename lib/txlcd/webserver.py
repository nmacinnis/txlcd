#from twisted.internet import reactor
#from twisted.request import TwistedRequest
from twisted.web import resource

class Webserver(resource.Resource):
    isLeaf = True
    def __init__(self, logger=None, button_masher=None):
        self.logger = logger
        self.button_masher = button_masher

    def render_GET(self, request):
        self.logger.debug(request)
        current_message = self.button_masher.message
        render = '<html>%s</html>' % current_message.message_text
        self.logger.debug(render)
        return str(render)
        #twisted_request = TwistedRequest(request=request)


