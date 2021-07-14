#!/usr/bin/env python


from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime

from datetime import datetime

from . import Base


class Status(Base):
    __tablename__ = "status"
    StatusId = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey("user.UserId"))
    LastUpdate = Column(DateTime, onupdate=datetime.now)
    StatusText = Column(String)

    def __repr__(self):
        return (
            f"<Status(StatusId={self.UserId},"
            f"UserId={self.UserId},"
            f"LastUpdate={self.LastUpdate},"
            f"StatusText={self.StatusText})>"
        )
