"""
these tests should cover functions and classes in robin.py
"""
import sqlite3
import pytest
from mock import AsyncMock, patch
from bot.modules.robin import Robin
import bot.modules.db as db

db.session = db.init()
TESTSTRING = "Dit is een teststring"
robin = Robin(db=db)


def test_usermap():
    """
    These tests will test update usermap.
    """
    new_user = db.User(
        UserId=1,
        DiscordAlias="discordalias1",
        GsheetAlias="gsheetalias1",
        LastChannel="lastchannel1",
    )
    db.session.add(new_user)
    res = robin._getusermap(1)
    assert res["DiscordAlias"] == "discordalias1"
