#!/usr/bin/env python


from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime

from datetime import datetime
from . import Base


class WSComeback(Base):
    __tablename__ = 'wscomeback'
    ComebackId = Column(Integer, primary_key=True)
    Id = Column(Integer, ForeignKey('usermap.Id'))
    WSId = Column(String(5))
    ShipType = Column(String(12))
    ReturnTime = Column(DateTime)
    NotificationTime = Column(DateTime)
