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


def testnormalize_time_():
    """
    check to see normalized time in "u" time from now (als huidige tijd voor 18:30 dan vandaag anders morgen..)
    """
    now = datetime.datetime.now()
    time = normalize_time("18:00u")
    hour = now.strftime("%H")
    if int(hour) >= 18:
        res_time = now + datetime.timedelta(days=1)
    else:
        res_time = now
    res_time = res_time.strftime("%Y-%m-%d 18:00")
    assert time == res_time
