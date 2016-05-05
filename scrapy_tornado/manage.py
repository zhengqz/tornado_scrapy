#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Created on 2016/05/05
Author: shylock
"""

import sys
import logging
import tornado.log
from tornado.options import options, define
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

from crawl.application import Application

define("port", default=8080, help="server on specify port", type=int)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    channel = logging.StreamHandler(sys.stdout)
    options.parse_command_line()
    channel.setFormatter(tornado.log.LogFormatter())
    logger.addHandler(channel)

    http_server  = HTTPServer(Application)
    http_server.listen(options.port)
    http_server.start()
    IOLoop.instance().start()