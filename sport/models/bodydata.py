# -*- coding: utf-8 -*-

import basic

from sqlalchemy import Table, Column, Integer
from sqlalchemy import DateTime, Interval
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base



class BodyData(Base):
    __tablename__ = "body_data"
    id = Column(Integer, primary_key=True)
    effort = Column(Integer)
    pulsation = Column(Integer)
    blood_pressure = Column(Integer)
    comment_id = Column(Integer, ForeignKey(basic.Comment.id))
