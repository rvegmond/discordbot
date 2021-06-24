#!/usr/bin/env python


from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime

from datetime import datetime

from . import Base


class Status(Base):
    __tablename__ = "status"
    StatusId = Column(Integer, primary_key=True)
    Id = Column(Integer, ForeignKey('usermap.Id'))
    LastUpdate = Column(DateTime, onupdate=datetime.now)
    StatusText = Column(String)
