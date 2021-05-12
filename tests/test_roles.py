import unittest
import pytest
from mock import AsyncMock, MagicMock
from mock.mock import patch
from bot.modules.roles import Roles


@pytest.mark.asyncio
@patch('bot.modules.roles.Roles._feedback')
async def test_get_all_roles(mocked_feedback):
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
    roles = Roles()
    req_role = "other_role"
    role = MagicMock()
    role.name = 'testrole'
    ctx = MagicMock()
    ctx.author.roles = [role]
    res = await roles.in_role(ctx, req_role)
    assert res is False


@pytest.mark.asyncio
async def test_in_role_nok():
    roles = Roles()
    req_role = "other_role"
    role = MagicMock()
    role.name = 'testrole'
    ctx = MagicMock()
    ctx.author.roles = [role]
    res = await roles.in_role(ctx, req_role)
    assert res is False
