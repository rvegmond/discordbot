import pytest
from mock import AsyncMock, MagicMock, patch


def mock_decorator():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)
        return decorated_function
    return decorator


patch('discord.ext.commands.command', mock_decorator).start()
# !important thing - import of app after patch()
from bot.modules.ping import Ping


def patched_command(*args):
    print("patched")
    return

@pytest.mark.asyncio
@patch('bot.modules.ping.Ping._feedback')
async def test_ping(mocked_feedback):
    # self = AsyncMock()
    ping = Ping()
    ctx = AsyncMock()
    await ping.ping(ctx)
    mocked_feedback.assert_called_once_with(ctx, msg='pong')
    patch.stopall


