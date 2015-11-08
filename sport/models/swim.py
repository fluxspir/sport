# -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer, String, Boolean
from sqlalchemy import DateTime, Interval
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

class Swim(Base):
    __tablename__ = "pool"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    duration = Column(Interval)
    swim_type = Colum(Integer, nullable=False)
    distance = Column(Integer)
    bodydatas = relationship("BodyData")
    set_id = Column(Integer, ForeignKey(Set.id))

class BodyData(Base):
    __tablename__ = "body_data"
    id = Column(Integer, primary_key=True)
    effort = Column(Integer)
    pulsation = Column(Integer)
    blood_pressure = Column(String)
