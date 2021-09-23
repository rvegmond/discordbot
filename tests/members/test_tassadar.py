"""
testing tassadar
"""
import pytest
import unittest
from mock import AsyncMock, patch
from bot.modules.members.tassadar import Tassadar


@pytest.mark.asyncio
@patch("bot.modules.members.tassadar.feedback")
async def test_tassadar(mocked_feedback):
    """
    test_ping, expecting pong
    """
    tassadar = Tassadar()
    ctx = AsyncMock()
    await tassadar.command(ctx)
    mocked_feedback.assert_called_once_with(
        ctx, msg="(https://www.youtube.com/watch?v=rBDwUXi1Sbw)"
    )
