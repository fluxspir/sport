# -*- coding: utf-8 -*-
#

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# This variable gets populated by models.init(). It is shared across the entire
# application and serves as the main session.
session = None
