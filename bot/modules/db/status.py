"""
This file contains the Status table definition
"""

from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime
from datetime import datetime
from . import Base


class Status(Base):
    """
    This file contains the Status table definition
    """

    __tablename__ = "status"
    StatusId = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey("user.UserId"))
    LastUpdate = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    StatusText = Column(String)

    def __repr__(self):
        """
        define return for table
        """
        return (
            f"<Status(StatusId={self.StatusId},"
            f"UserId={self.UserId},"
            f"LastUpdate={self.LastUpdate},"
            f"StatusText={self.StatusText})>"
        )
