"""
This file contains the WSTemp table definition
"""

from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime
from datetime import datetime
from . import Base


class WSTemp(Base):
    """
    This file contains the WSTemp table definition
    """

    __tablename__ = "wstemp"
    UserId = Column(Integer, ForeignKey("user.UserId"), primary_key=True)

    def __repr__(self):
        """
        define return for table
        """
        return f"<WSTemp(UserId={self.UserId}>"
