#!/usr/bin/env python


from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime

from datetime import datetime
from . import Base


class RSQueue(Base):
    __tablename__ = "rsqueue"
    QueueId = Column(Integer, primary_key=True)
    DiscordId = Column(Integer)
    # UserId = Column(Integer, ForeignKey("user.UserId"))
    RSLevel = Column(Integer)
    Runtime = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return (
            f"<RSQueue(QueueId={self.QueueId},"
            f"RSQueue(DiscordId={self.DiscordId},"
            f"RSQueue(RSLevel={self.RSLevel},"
            f"RsQueue(Runtime={self.Runtime}>"
        )
