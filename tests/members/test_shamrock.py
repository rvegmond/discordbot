"""
testing tassadar
"""
import pytest
import unittest
from mock import AsyncMock, patch
from bot.modules.members.shamrock import Shamrock


@pytest.mark.asyncio
@patch("bot.modules.members.shamrock.feedback")
async def test_shamrock(mocked_feedback):
    """
    test_ping, expecting pong
    """
    shamrock = Shamrock()
    ctx = AsyncMock()
    await shamrock.command(ctx)
    mocked_feedback.assert_called_once_with(
        ctx,
        msg="Voelt zich niet zo lekker,\n had gister dat laatste biertje niet moeten nemen...",
    )
