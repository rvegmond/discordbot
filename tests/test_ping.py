"""
testing the functions and classes in ping.py
"""
import pytest
import unittest
from mock import AsyncMock, patch
from bot.modules.ping import Ping


@pytest.mark.asyncio
@patch("bot.modules.ping._feedback")
async def test_ping(mocked_feedback):
    """
    test_ping, expecting pong
    """
    ping = Ping()
    ctx = AsyncMock()
    await ping.ping(ctx)
    mocked_feedback.assert_called_once_with(ctx, msg="pong")


class Test(unittest.TestCase):
    @pytest.mark.asyncio
    @patch("bot.modules.ping._feedback")
    async def test_ping(self, mocked_feedback):
        """
        test_ping, expecting pong
        """
        ping = Ping()
        ctx = AsyncMock()
        await ping.ping(ctx)
        mocked_feedback.assert_called_once_with(ctx, msg="pong")
