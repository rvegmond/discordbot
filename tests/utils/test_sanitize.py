"""
these tests should cover functions and classes in robin.py
"""
import pytest
from mock import AsyncMock, patch
from bot.modules.utils import sanitize

TESTSTRING = "Dit is een teststring"


def test_sanitize():
    """
    These tests will check if the strings get sanitized properly.
    """
    assert sanitize(msg_in=TESTSTRING) == TESTSTRING
    assert sanitize(msg_in=TESTSTRING + "met een at @") == TESTSTRING + "met een at _"
    assert sanitize(msg_in="TestString met een hash #") == "TestString met een hash _"
    assert (
        sanitize(msg_in="TestString met een lange string", maxlength=20)
        == "TestStr .. truncated"
    )
    assert sanitize(msg_in="Korte TestString", maxlength=12) == " .. truncated"
