# -*- coding: utf-8 -*-

import datetime

from meta import Base
import basic
import bodydata

from sqlalchemy import Table, Column, Integer, Float, String
from sqlalchemy import DateTime, Interval
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class Swim(Base):
    __tablename__ = "swim"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class SwimData(Base):
    __tablename__ = "swim_data"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.now())
    swim_id = Column(Integer, ForeignKey(Swim.id), nullable=False)
    swim = relationship("Swim")
    start = Column(DateTime)
    duration = Column(Interval)
    distance = Column(Float)
    bodydata_id = Column(Integer, ForeignKey(bodydata.Cardio.id))
    bodydatas = relationship("Cardio")
    set_id = Column(Integer, ForeignKey(basic.Set.id))
    comments_id = Column(Integer, ForeignKey(basic.Comment.id))
    comment = relationship("Comment")

