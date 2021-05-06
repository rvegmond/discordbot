import unittest
import pytest
from mock import MagicMock
from modules.whitestar import WhiteStar
import datetime 

bot = MagicMock()


def test_normalize_time():
    whitestar = WhiteStar(bot)
    now = datetime.datetime.now()
    time = whitestar._normalize_time("18:00")
    res_time = now + datetime.timedelta(hours=18)
    res_time = res_time.strftime("%Y-%m-%d %H:%M")
    assert time == res_time

# @pytest.mark.asyncio
# async def test_update_usermap():
#     """
#     Need to write the test, using mock db
#     """
#     whitestar = WhiteStar(bot)
#     ctx = MagicMock()
#     role = MagicMock()
#     role.name = 'testrole'
#     res = True
#     assert res is True
