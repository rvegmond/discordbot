"""
these tests should cover functions and classes in roles.py
"""
import pytest
from mock import AsyncMock, MagicMock
from mock.mock import patch
from bot.modules.utils import in_role


@pytest.mark.asyncio
async def test_in_role_ok():
    """
    Testing to see if the user is in the specified role.
    """
    req_role = "testrole"
    role = MagicMock()
    role.name = req_role
    ctx = MagicMock()
    ctx.author.roles = [role]
    res = await in_role(ctx, req_role)
    assert res is True


@pytest.mark.asyncio
async def test_in_role_nok():
    """
    Testing to see if the user is not in the specified role.
    """
    req_role = "other_role"
    role = MagicMock()
    role.name = "testrole"
    ctx = MagicMock()
    ctx.author.roles = [role]
    res = await in_role(ctx, req_role)
    assert res is False
