"""
Testing normalize_time
"""
import datetime
import pytest
from bot.modules.utils import normalize_time


def testnormalize_time_colon():
    """
    check to see normalized time in "clock" time from now
    """
    now = datetime.datetime.now()
    time = normalize_time("18:30")
    res_time = now + datetime.timedelta(hours=18, minutes=30)
    res_time = res_time.strftime("%Y-%m-%d %H:%M")
    assert time == res_time


def testnormalize_time_dot():
    """
    check to see normalized time in "dot" time from now
    """
    now = datetime.datetime.now()
    time = normalize_time("18.5")
    res_time = now + datetime.timedelta(hours=18, minutes=30)
    res_time = res_time.strftime("%Y-%m-%d %H:%M")
    assert time == res_time
