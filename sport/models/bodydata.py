# -*- coding: utf-8 -*-
#

from meta import Base
import basic

from sqlalchemy import Table, Column, Integer
from sqlalchemy import DateTime, Interval
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base



class Cardio(Base):
    __tablename__ = "cardio"
    id = Column(Integer, primary_key=True)
    effort = Column(Integer)
    pulsation = Column(Integer)
    blood_pressure = Column(Integer)
    comment_id = Column(Integer, ForeignKey(basic.Comment.id))
    comment = relationship("Comment")
