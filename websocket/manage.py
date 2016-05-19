#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Created on 2016/05/19
Author: Atom
"""

import tornado.web
import tornado.websocket
import tornado.ioloop

import re
import os
import commands
import json
import threading
import subprocess


def vmstat():
    io_loop = tornado.ioloop.IOLoop.instance()
    mem_key = ["sw", "free", "buff", "cache", "total"]
    cpu_key = ["us", "sy", "id", "wa"]
    disk_key = ["total", "used", "avail", "percent"]
    space = re.compile("\s+")
    mem_total_shell = r"""cat /proc/meminfo | grep MemTotal | sed 's/\w*:\s*\([0-9]*\).*/\1/'"""
    mem_total = subprocess.check_output(mem_total_shell, shell=True).strip()
    p_vmstat = subprocess.Popen(['vmstat', '1', '-n'], stdout=subprocess.PIPE)
    p_vmstat.stdout.readline()
    p_vmstat.stdout.readline()
    for line in iter(p_vmstat.stdout.readline, ""):
        fields = space.split(line.strip())
        mem_val = fields[2:6]
        mem_val.append(mem_total)
        disk_val = get_disk_space()
        cpu_val = fields[-5:-1]
        result = dict(memory=dict(zip(mem_key, mem_val)),
                      disk=dict(zip(disk_key, disk_val)),
                      cpu=dict(zip(cpu_key, cpu_val)),
                      uptime=get_running_time())
        result = json.dumps(result)
        for client in MonitorHandler.clients:
            io_loop.add_callback(client.write_message, result)


def get_running_time():
    return commands.getoutput("uptime")


def get_disk_space():
    disk = commands.getoutput("df -h /").split()
    return disk[-5:-1]


class MonitorHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def check_origin(self, origin):
        return True

    def open(self, *args, **kwargs):
        MonitorHandler.clients.add(self)
        print("clients: %s online." % (len(MonitorHandler.clients)))

    def on_message(self, message):
        pass

    def on_close(self):
        MonitorHandler.clients.remove(self)
        print("clients: %s online." % len(MonitorHandler.clients))


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("index.html")


settings = {
    'debug': True,
    "template_path": os.path.join(os.path.dirname(__file__), 'templates'),
    "static_path": os.path.join(os.path.dirname(__file__), 'static'),
    "gzip": True
}

handlers = [
    (r'/', IndexHandler),
    (r'/ws', MonitorHandler)
]

application = tornado.web.Application(handlers, **settings)
if __name__ == "__main__":
    application.listen(8001,address="106.2.108.77")
    t = threading.Thread(target=vmstat)
    t.daemon = True
    t.start()
    tornado.ioloop.IOLoop.instance().start()
