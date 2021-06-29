#!/usr/bin/env python


from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey, DateTime

from datetime import datetime
from . import Base


class UserMap(Base):
    __tablename__ = "usermap"
    UserId = Column(Integer, primary_key=True)
    DiscordId = Column(String)
    DiscordAlias = Column(String)
    GsheetAlias = Column(String)
