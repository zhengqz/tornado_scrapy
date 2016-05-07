#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
Created on 2016/05/07
Author: shylock
"""

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    votes = Column(Integer, default=0)
    body = Column(String)
    tags = Column(String)
    link = Column(String)
