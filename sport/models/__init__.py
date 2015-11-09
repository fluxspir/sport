# -*- coding: utf-8 -*-
#

import meta
import sqlalchemy
import ConfigParser
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import ZopeTransactionExtension

from basic import Comment, Session, Set
from swim import Swim
from run import Run
from bodydata import BodyData

def init():
    parser = ConfigParser.ConfigParser()
    home = os.path.expanduser("~")
    parser.read(os.path.join(home, ".franckdbrc"))
    db_url = parser.get("sport", "db_url")

    engine = create_engine(db_url, echo=False, convert_unicode=True)
    Session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))

    meta.session = Session()
