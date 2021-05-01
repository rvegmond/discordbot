import unittest
import pytest
from mock import MagicMock
from modules.whitestar import WhiteStar

bot = MagicMock()

# @pytest.mark.asyncio
# async def test_update_comeback_channel():
#     whitestar = Whitestar()

#     assert res is True

@pytest.mark.asyncio
async def test_update_usermap():
    """
    Need to write the test, using mock db
    """
    whitestar = WhiteStar(bot)
    ctx = MagicMock()
    role = MagicMock()
    role.name = 'testrole'
    res = True
    assert res is True
