import pytest
from mock import AsyncMock, MagicMock, patch
from bot.modules.ping import Ping


@pytest.mark.asyncio
@patch('bot.modules.ping.Ping._feedback')
async def test_ping(mocked_feedback):
    ping = Ping()
    ctx = AsyncMock()
    await ping._ping(ctx)
    mocked_feedback.assert_called_once_with(ctx, msg='pong')
