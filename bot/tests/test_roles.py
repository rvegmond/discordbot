import unittest
import pytest
from mock import MagicMock
from modules.roles import Roles
from mock.mock import patch


def test_get_roles():
    self = MagicMock()
    roles = Roles()
    req_role = "testrole"
    role = MagicMock()
    role.name = req_role
    ctx = MagicMock()
    ctx.guild.roles = [role]
    res = roles._get_roles(ctx)
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
