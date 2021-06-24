"""
This directory contains modules.
"""
# import os
# import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# sys.path.append(os.path.dirname(os.path.realpath(__file__)))

Base = declarative_base()

from .status import Status
from .usermap import UserMap
from .wscomeback import WSComeback
from .wsentry import WSEntry

_DB_URI = 'sqlite:///:memory:'
engine = create_engine(_DB_URI, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
