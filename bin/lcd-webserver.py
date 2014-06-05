#!/usr/bin/env python
import logging
import txroutes

#from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from twisted.internet import reactor
from twisted.web.server import Site

from txlcd.buttonmasher import ButtonMasher
from txlcd.lcd import MockLcd
from txlcd.model import Model
from txlcd.webserver import Controller

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    datastore = 'sqlite:///db.sqlite'
    model = Model(logger=logger, datastore=datastore)

    #lcd = Adafruit_CharLCDPlate(busnum=1)
    lcd = MockLcd(logger=logger)

    button_masher = ButtonMasher(logger=logger, model=model, lcd=lcd)

    controller = Controller(logger=logger, button_masher=button_masher)
    dispatcher = txroutes.Dispatcher(logger=logger)

    dispatcher.connect('get_index', '/', controller=controller,
            action='get_index', conditions=dict(method=['GET']))


    site = Site(dispatcher)
    reactor.listenTCP(8090, site)

    reactor.callLater(.1, button_masher.start_button_checker)
    reactor.callLater(.1, button_masher.start_screen_lighter)

    def stop_threads():
        button_masher.checking = False
        logger.info("shutting down")

    reactor.addSystemEventTrigger('before', 'shutdown', stop_threads)

    logger.info("starting webserver")
    reactor.run()
