#!/usr/bin/env python


from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime

from datetime import datetime

from . import Base


class Status(Base):
    __tablename__ = "status"
    StatusId = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey('usermap.UserId'))
    LastUpdate = Column(DateTime, onupdate=datetime.now)
    StatusText = Column(String)
