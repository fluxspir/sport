# -*- coding: utf-8 -*-

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


