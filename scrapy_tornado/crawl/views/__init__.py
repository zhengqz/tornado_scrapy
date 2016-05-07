#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Created on 2016/05/05
Author: shylock
"""

from .api import api_routes
from .base import base_routes

urls = []

urls += api_routes
urls += base_routes
