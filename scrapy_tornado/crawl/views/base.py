#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Created on 2016/05/05
Author: shylock
"""

from tornado import web
from tornado import template
import json
from bson import json_util
import logging

base_routes = []

class BaseHandler(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)

    @property
    def db(self):
        return self.application.db

    @property
    def rdc(self):
        return self.application.rdc

    @property
    def loader(self):
        return template.Loader(self.application.template)

    def render_error(self, code, msg):
        data = {"code": code, "detail": msg}
        self.write_json(data)

    def load_body(self):
        try:
            data = json.loads(self.request.body)
        except Exception, e:
            logging.error(e)
            return None
        return data

    def write_json(self, data):
        msg = json.dumps(data, default=json_util.default)
        self.write(msg)
