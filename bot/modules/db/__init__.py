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
from .rsqueue import RSQueue


def init(db_uri: str = "sqlite://"):
    engine = create_engine(db_uri, echo=True)
    Base.metadata.create_all(engine)
    dbsession = sessionmaker(bind=engine)
    return dbsession()
