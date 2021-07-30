"""
these tests should cover functions and classes in roles.py
"""
import pytest
from mock import AsyncMock, MagicMock
from mock.mock import patch
from bot.modules.utils import GetAllRoles


@pytest.mark.asyncio
@patch("bot.modules.utils.get_all_roles.feedback")
async def test_get_all_roles(mocked_feedback):
    """
    Testing to see if can get a listed output of all roles.
    """
    get_all_roles = GetAllRoles()
    context = AsyncMock()
    role = MagicMock()
    req_role = "testrole"
    role.name = req_role
    context.guild.roles = [role]
    await get_all_roles.command(context)
    mocked_feedback.assert_called_once_with(context, msg="role.name: testrole\n")
