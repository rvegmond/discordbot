"""
This directory contains modules.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

from .status import Status
from .user import User
from .wscomeback import WSComeback
from .wsentry import WSEntry
from .wstemp import WSTemp

_DB_URI = "sqlite:///hades.db"
engine = create_engine(_DB_URI, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
