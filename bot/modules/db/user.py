#!/usr/bin/env python


from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime

from datetime import datetime
from . import Base


class User(Base):
    __tablename__ = "user"
    UserId = Column(Integer, primary_key=True)
    DiscordId = Column(String)
    DiscordAlias = Column(String)
    DiscordNick = Column(String)
    GsheetAlias = Column(String)
    LastActive = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    LastChannel = Column(String)

    def __repr__(self):
        return (
            f"<User(UserId={self.UserId},"
            f"DiscordId={self.DiscordId},"
            f"DiscordAlias={self.DiscordAlias},"
            f"DiscordNick={self.DiscordNick},"
            f"GsheetAlias={self.GsheetAlias},"
            f"LastActive={self.LastActive},"
            f"LastChannel={self.LastChannel})>"
        )
