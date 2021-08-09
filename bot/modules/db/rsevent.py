#!/usr/bin/env python


from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime

from datetime import datetime
from . import Base


class RSEvent(Base):
    __tablename__ = "rsevent"
    EventId = Column(Integer, primary_key=True)
    DiscorId = Column(Integer)
    RSLevel = Column(Integer)
    Runtime = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return (
            f"<RSEvent(EventId={self.EventId},"
            f"RSEvent(DiscordId={self.DiscordId},"
            f"RSEvent(RSLevel={self.RSLevel},"
            f"RsEvent(Runtime={self.Runtime}>"
        )
