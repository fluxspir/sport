# -*- coding: utf-8 -*-
#

class Run(Base):
    __tablename__ = "run"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    duration = Column(Interval)
    distance = Column(Integer)
    bodydatas = relationship("BodyData")
    set_id = Column(Integer, ForeignKey(Set.id))


