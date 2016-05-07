#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Created on 2016/05/07
Author: shylock
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis

engine = create_engine("mysql+mysqldb://root:root@localhost:3306/spider?charset=utf8")
DBSession = sessionmaker(engine)
Redis = redis.StrictRedis(host="",port=6379, db=0)