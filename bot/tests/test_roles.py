import unittest
import pytest
from mock import MagicMock
from modules.roles import Roles
from mock.mock import patch


# @pytest.mark.asyncio
# async def test_get_roles_ok():
#     roles = Roles()
#     role = MagicMock()
#     role.name = 'testrole'
#     ctx = MagicMock()
#     ctx.guild.fetch_roles.return_value = [role]
#     res = await roles._get_roles(ctx)
#     assert res is f"role.name: testrole"


@pytest.mark.asyncio
async def test_in_role_ok():
    roles = Roles()
    req_role = "testrole"
    role = MagicMock()
    role.name = 'testrole'
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


# def test_in_role():
#     roles = Roles()
#     role_name = 'testrole'
#     role = MagicMock()
#     role.role_name = role_name
#     ctx = MagicMock()
#     ctx.author.roles = [role]

#     with patch("discord.utils.get(guild.roles)", return_value=members):
#         res = roles._rolemembers(ctx, role_name)
#     assert res == members


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
