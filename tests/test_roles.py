"""
these tests should cover functions and classes in roles.py
"""
import pytest
from mock import AsyncMock, MagicMock
from mock.mock import patch
from bot.modules.roles import Roles, _rolemembers


@pytest.mark.asyncio
@patch('bot.modules.roles.Roles._feedback')
async def test_get_all_roles(mocked_feedback):
    """
    Testing to see if can get a listed output of all roles.
    """
    roles = Roles()
    ctx = AsyncMock()
    role = MagicMock()
    req_role = "testrole"
    role.name = req_role
    ctx.guild.roles = [role]
    await roles.get_all_roles(ctx)
    mocked_feedback.assert_called_once_with(ctx, msg='role.name: testrole\n')


@pytest.mark.asyncio
async def test_in_role_ok():
    """
    Testing to see if the user is in the specified role.
    """
    roles = Roles()
    req_role = "testrole"
    role = MagicMock()
    role.name = req_role
    ctx = MagicMock()
    ctx.author.roles = [role]
    res = await roles.in_role(ctx, req_role)
    assert res is True


@pytest.mark.asyncio
async def test_in_role_nok():
    """
    Testing to see if the user is not in the specified role.
    """
    roles = Roles()
    req_role = "other_role"
    role = MagicMock()
    role.name = 'testrole'
    ctx = MagicMock()
    ctx.author.roles = [role]
    res = await roles.in_role(ctx, req_role)
    assert res is False


def test_get_rolemembers():
    """
    Testing to see if we receive the right rolemembers
    """
    ctx = MagicMock()
    role = MagicMock()
    member1 = MagicMock()
    member1.id = 'testuser1'
    member2 = MagicMock()
    member2.id = 'testuser2'
    req_role = "testrole"
    role.name = req_role
    role.members = [member1, member2]
    ctx.guild.roles = [role]
    result = _rolemembers(ctx, req_role)
    assert result == ['testuser1', 'testuser2']
