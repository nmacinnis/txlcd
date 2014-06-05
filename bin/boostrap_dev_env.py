#!/usr/bin/env python
import IPython
import logging
import requests
import threading
import txroutes

from twisted.internet import reactor
from twisted.web.server import Site

from txlcd.buttonmasher import ButtonMasher
from txlcd.lcd import MockLcd
from txlcd.model import Model
from txlcd.webserver import Controller

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


datastore = 'sqlite:///db.sqlite'
model = Model(logger=logger, datastore=datastore)

lcd = MockLcd(logger=logger)

button_masher = ButtonMasher(logger=logger, model=model, lcd=lcd)

controller = Controller(logger=logger, button_masher=button_masher)
dispatcher = txroutes.Dispatcher(logger=logger)

dispatcher.connect('get_index', '/', controller=controller,
        action='get_index', conditions=dict(method=['GET']))


site = Site(dispatcher)
reactor.listenTCP(8090, site)



def start_button_masher():
    reactor.callLater(.1, button_masher.start_button_checker)
    reactor.callLater(.1, button_masher.start_screen_lighter)

def stop_button_masher():
    button_masher.checking = False

start_button_masher()
reactor.addSystemEventTrigger('before', 'shutdown', stop_button_masher)

def press_a_button(b):
    lcd.button = b
    def unpress():
        lcd.button = None
    reactor.callLater(.2, unpress)

_current_thread = threading.current_thread()

def _start_reactor_in_thread():
    thread = threading.Thread(target=reactor.run, args=(False,))
    thread.start()
    logger.info("reactor started")
    return thread

def _stop_reactor():
    if not reactor.running:
        logger.info("reactor not running")
        return
    reactor.callFromThread(reactor.stop)
    reactor.runUntilCurrent()
    logger.info("reactor stopped")

def _stop_reactor_on_exit():
    _current_thread.join()
    _stop_reactor()

_start_reactor_in_thread()
threading.Thread(target=_stop_reactor_on_exit).start()

requests.get('http://localhost:8090')

IPython.embed()
