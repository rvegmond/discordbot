import pytest
from mock import MagicMock, patch
from modules.ping import Ping


@pytest.mark.asyncio
@patch('modules.ping.Ping._feedback')
async def test_ping(mocked_feedback):
    ping = Ping()
    ctx = MagicMock()
    await ping._ping(ctx)
    mocked_feedback.assert_called_once_with(ctx, msg='pong')
