import unittest
import pytest
from mock import AsyncMock, MagicMock
from bot.modules.whitestar import WhiteStar
import datetime 
from mock.mock import patch

bot = MagicMock()


def test_normalize_time_colon():
    whitestar = WhiteStar(bot)
    now = datetime.datetime.now()
    time = whitestar._normalize_time("18:30")
    res_time = now + datetime.timedelta(hours=18, minutes=30)
    res_time = res_time.strftime("%Y-%m-%d %H:%M")
    assert time == res_time


def test_normalize_time_dot():
    whitestar = WhiteStar(bot)
    now = datetime.datetime.now()
    time = whitestar._normalize_time("18.5")
    res_time = now + datetime.timedelta(hours=18, minutes=30)
    res_time = res_time.strftime("%Y-%m-%d %H:%M")
    assert time == res_time


# @pytest.mark.asyncio
# async def test_update_comeback_channel():
#     whitestar = WhiteStar(bot)
#     nu = str("2021-05-31 12:00")
#     result = ['John', 'BS', nu, nu]
#     comeback_channel = AsyncMock()
#     whitestar.conn = MagicMock()
#     ctx = MagicMock()
#     whitestar.conn = MagicMock()
#     whitestar.conn.cursor().fetchall.return_value = result
#     res = await whitestar._update_comeback_channel(comeback_channel, 'ws_')
#     # comeback_channel.assert_called_once_with('John')


def test_dummy():
    whitestar = WhiteStar(bot)
    result = ['John', 'Bill']
    whitestar.conn = MagicMock()
    ctx = MagicMock()
    whitestar.conn = MagicMock()
    whitestar.conn.cursor().fetchall.return_value = result
    res = whitestar.dummy(ctx)
    assert res[0] == 'John'


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
