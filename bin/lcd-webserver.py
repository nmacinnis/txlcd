#!/usr/bin/env python
import logging

from twisted.internet import reactor
from twisted.web.server import Site

from txlcd.webserver import Webserver

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    site = Site(Webserver(logger=logger))
    reactor.listenTCP(8090, site)
    reactor.run()
