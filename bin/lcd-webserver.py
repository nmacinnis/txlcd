#!/usr/bin/env python
import logging

from twisted.internet import reactor
from twisted.web.server import Site

from txlcd.buttonmasher import ButtonMasher
from txlcd.model import Model
from txlcd.webserver import Webserver

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    datastore = 'sqlite:///db.sqlite'
    model = Model(logger=logger, datastore=datastore)

    site = Site(Webserver(logger=logger))
    reactor.listenTCP(8090, site)

    button_masher = ButtonMasher(logger=logger, model=model)
    reactor.callLater(.1, button_masher.start_button_checker)
    reactor.run()
