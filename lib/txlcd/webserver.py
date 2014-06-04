#from twisted.internet import reactor
#from twisted.request import TwistedRequest
from twisted.web import resource

class Webserver(resource.Resource):
    isLeaf = True
    def __init__(self, logger=None):
        self.logger = logger

    def render_GET(self, request):
        self.logger.debug(request)
        return '<html>Derp</html>'
        #twisted_request = TwistedRequest(request=request)


