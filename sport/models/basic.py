# -*- coding: utf-8 -*-

import datetime

from meta import Base

from sqlalchemy import Table, Column, Integer, String
from sqlalchemy import DateTime, Interval
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    comment = Column(String, nullable=False)

class Place(Base):
    __tablename__ = "place"
    id = Column(Integer, primary_key=True)
    place = Column(String, nullable=False)
    comment_id = Column(Integer, ForeignKey(Comment.id))
    comment = relationship("Comment")
    last_use = Column(DateTime, nullable=False)

class Session(Base):
    __tablename__ = "session"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.now())
    start = Column(DateTime, nullable=False)
    duration = Column(Interval, nullable=False)
    comment_id = Column(Integer, ForeignKey(Comment.id))
    comment = relationship("Comment")
    place_id = Column(Integer, ForeignKey(Place.id))
    sets = relationship("Set", backref="session")

class Set(Base):
    __tablename__ = "set"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.now())
    start = Column(DateTime)
    duration = Column(Interval)
    sequence = Column(Integer, nullable=False)
    session_id = Column(Integer, ForeignKey(Session.id), nullable=False)
    comment_id = Column(Integer, ForeignKey(Comment.id))
    comment = relationship("Comment")
