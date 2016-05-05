#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Created on 2016/05/05
Author: shylock
"""

import tornado.web
import motor
from tornado import template
import redis
from . import settings as config
from .views import urls


class Application(tornado.web.Application):
    def __init__(self):
        redis_uri = config.REDIS_URI

        settings = dict(
            static_path=config.STATIC_PATH,
            xsrf_cookies=False,
            cookie_secret=config.COOKIE_STR,
            login_url="/u/login",
            autoscape=None,
        )

        self.rdc = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)
        self.db = motor.MotorClient(config.MONGO_URI).zhihu
        self.template = template.Loader(config.TEMPLATE)

        super(Application, self).__init__(urls, **settings)
