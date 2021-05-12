import unittest
import pytest
from mock import AsyncMock, MagicMock
from mock.mock import patch
from bot.modules.roles import Roles

# @pytest.mark.asyncio
# @patch('bot.modules.roles.Roles._feedback')
# async def test_tza(mocked_feedback):
#     self = AsyncMock()
#     roles = Roles()
#     req_role = "testrole"
#     role = MagicMock()
#     role.name = req_role
#     ctx = AsyncMock()
#     ctx.guild.roles = [role]
#     await roles.tza(self, ctx)
#     mocked_feedback.assert_called_once_with(ctx, msg='role.name: testrole fout\n')


def test_get_all_roles():
    self = MagicMock()
    roles = Roles()
    req_role = "testrole"
    role = MagicMock()
    role.name = req_role
    ctx = MagicMock()
    ctx.guild.roles = [role]
    res = roles._get_all_roles(ctx)
    assert res == "role.name: testrole\n"


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
