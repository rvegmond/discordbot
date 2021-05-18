"""
these tests should cover functions and classes in robin.py
"""
import datetime
from mock import MagicMock
from bot.modules.whitestar import WhiteStar, _normalize_time

bot = MagicMock()


def test_normalize_time_colon():
    """
    check to see normalized time in "clock" time from now
    """
    now = datetime.datetime.now()
    time = _normalize_time("18:30")
    res_time = now + datetime.timedelta(hours=18, minutes=30)
    res_time = res_time.strftime("%Y-%m-%d %H:%M")
    assert time == res_time


def test_normalize_time_dot():
    """
    check to see normalized time in "dot" time from now
    """
    now = datetime.datetime.now()
    time = _normalize_time("18.5")
    res_time = now + datetime.timedelta(hours=18, minutes=30)
    res_time = res_time.strftime("%Y-%m-%d %H:%M")
    assert time == res_time


# def test_dummy():
#     """
#     Dummy test to experiment with testing.
#     """
#     whitestar = WhiteStar(bot)
#     result = [['John', 'Bill']]
#     whitestar.conn = MagicMock()
#     ctx = MagicMock()
#     whitestar.conn = MagicMock()
#     whitestar.conn.cursor().fetchall.return_value = result
#     res = whitestar.dummy(ctx)
#     assert res == 'John'
