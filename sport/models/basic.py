# -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer
from sqlalchemy import DateTime, Interval
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base


class Session(Base):
    __tablename__ = "session"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.now())
    duration = Column(Interval)

class Set(Base):
    __tablename__ = "set"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    duration = Column(Interval)
    sequence = Column(Integer)
    session_id = Column(Integer, ForeignKey(Session.id))

