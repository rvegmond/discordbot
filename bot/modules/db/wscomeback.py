"""
This file contains the WSComeback table definition
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from . import Base


class WSComeback(Base):
    """
    This file contains the WSComeback table definition
    """

    __tablename__ = "wscomeback"
    ComebackId = Column(Integer, primary_key=True)
    UserId = Column(Integer, ForeignKey("user.UserId"))
    WSId = Column(String(5))
    ShipType = Column(String(12))
    ReturnTime = Column(DateTime)
    NotificationTime = Column(DateTime)

    def __repr__(self):
        """
        define return for table
        """
        return (
            f"<WSComeback(ComebackId={self.ComebackId},"
            f"UserId={self.UserId},"
            f"WSId={self.WSId},"
            f"ShipType={self.ShipType},"
            f"ReturnTime={self.ReturnTime},"
            f"NotificationTime={self.NotificationTime})>"
        )
