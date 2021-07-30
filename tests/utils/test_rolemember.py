"""
these tests should cover functions and classes in roles.py
"""
import pytest
from mock import AsyncMock, MagicMock
from mock.mock import patch
from bot.modules.utils import rolemembers


def test_get_rolemembers():
    """
    Testing to see if we receive the right rolemembers
    """
    ctx = MagicMock()
    role = MagicMock()
    member1 = MagicMock()
    member1.id = "testuser1"
    member2 = MagicMock()
    member2.id = "testuser2"
    req_role = "testrole"
    role.name = req_role
    role.members = [member1, member2]
    ctx.guild.roles = [role]
    result = rolemembers(ctx, req_role)
    assert result == ["testuser1", "testuser2"]
