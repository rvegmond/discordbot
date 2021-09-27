"""
testing the functions and classes in ping.py
"""
import pytest
import unittest
from mock import AsyncMock, patch
from bot.modules.utils.ping import Ping


@pytest.mark.asyncio
@patch("bot.modules.utils.ping.feedback")
async def test_ping(mocked_feedback):
    """
    test_ping, expecting pong
    """
    ping = Ping()
    ctx = AsyncMock()
    await ping.command(ctx)
    mocked_feedback.assert_called_once_with(ctx, msg="pong")
