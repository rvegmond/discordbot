"""
This file contains the User table definition
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from . import Base


class User(Base):
    """
    This file contains the User table definition
    """

    __tablename__ = "user"
    UserId = Column(Integer, primary_key=True)
    DiscordId = Column(String)
    DiscordAlias = Column(String)
    DiscordNick = Column(String)
    GsheetAlias = Column(String)
    LastActive = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    LastChannel = Column(String)

    def __repr__(self):
        """
        define return for table
        """
        return (
            f"<User(UserId={self.UserId},"
            f"DiscordId={self.DiscordId},"
            f"DiscordAlias={self.DiscordAlias},"
            f"DiscordNick={self.DiscordNick},"
            f"GsheetAlias={self.GsheetAlias},"
            f"LastActive={self.LastActive},"
            f"LastChannel={self.LastChannel})>"
        )

    def __str__(self):
        """
        Dummy function
        """
        return self.__class__.__name__
