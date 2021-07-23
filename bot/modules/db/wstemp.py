#!/usr/bin/env python


from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime

from datetime import datetime
from . import Base


class WSTemp(Base):
    __tablename__ = "wstemp"
    UserId = Column(Integer, ForeignKey("user.UserId"), primary_key=True)

    def __repr__(self):
        return f"<WSTemp(UserId={self.UserId}>"
