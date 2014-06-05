#!/usr/bin/env python
import logging

#from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from twisted.internet import reactor
from twisted.web.server import Site

from txlcd.buttonmasher import ButtonMasher
from txlcd.lcd import MockLcd
from txlcd.model import Model
from txlcd.webserver import Webserver

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    datastore = 'sqlite:///db.sqlite'
    model = Model(logger=logger, datastore=datastore)

    #lcd = Adafruit_CharLCDPlate(busnum=1)
    lcd = MockLcd(logger=logger)

    button_masher = ButtonMasher(logger=logger, model=model, lcd=lcd)

    webserver = Webserver(logger=logger, button_masher=button_masher)

    site = Site(webserver)
    reactor.listenTCP(8090, site)

    reactor.callLater(.1, button_masher.start_button_checker)
    reactor.callLater(.1, button_masher.start_screen_lighter)
    def stop_threads():
        button_masher.checking = False
        logger.info("shutting down")
    #reactor.addSystemEventTrigger('before', 'shutdown', lambda: button_masher.checking = False)
    reactor.addSystemEventTrigger('before', 'shutdown', stop_threads)

    logger.info("starting webserver")
    reactor.run()
