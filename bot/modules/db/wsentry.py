#!/usr/bin/env python


from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime

from datetime import datetime
from . import Base


class WSEntry(Base):
    __tablename__ = 'wsentry'
    EntryId = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey('usermap.UserId'))
    Remark = Column(String)
    EntryTime = Column(DateTime, onupdate=datetime.now)
    active = Column(Boolean, default=True)
