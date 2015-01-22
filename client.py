#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.ioloop import IOLoop
from tornado import gen
from tornado.websocket import websocket_connect


class Client(object):
    def __init__(self, url, timeout):
        self.url = url
        self.timeout = timeout
        self.ioloop = IOLoop.instance()
        self.ws = None
        self.connect()
        self.ioloop.start()

    @gen.coroutine
    def connect(self):
        print "trying to connect"
        try:
            self.ws = yield websocket_connect(self.url)
        except Exception, e:
            self.ioloop.call_later(self.timeout, self.connect)
        else:
            print "connected"
            self.run()

    @gen.coroutine
    def run(self):
        while True:
            msg = yield self.ws.read_message()
            if msg is None:
                print "connection closed"
                self.ws = None
                self.ioloop.call_later(self.timeout, self.connect)
                break
                

if __name__ == "__main__":
    client = Client("ws://localhost:3000", 5)
