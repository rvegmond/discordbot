import pytest
import sqlite3
from mock import MagicMock, Mock, patch, AsyncMock
from bot.modules.robin import Robin


def test_sanitize():
    robin = Robin()
    assert robin._sanitize(msg_in='Dit is een teststring') == 'Dit is een teststring'
    assert robin._sanitize(msg_in='TestString met een at @') == 'TestString met een at _'
    assert robin._sanitize(msg_in='TestString met een hash #') == 'TestString met een hash _'
    assert robin._sanitize(msg_in='TestString met een hash #') == 'TestString met een hash _'
    assert robin._sanitize(msg_in='TestString met een lange string', maxlength=20) == 'TestStr .. truncated'
    assert robin._sanitize(msg_in='Korte TestString', maxlength=12) == ' .. truncated'


@pytest.mark.asyncio
async def test_feedback():
    robin = Robin()
    ctx = AsyncMock()
    res = await robin._feedback(ctx=ctx, msg='Dit is een teststring')
    assert res == 'feedback sent successful'


@pytest.mark.asyncio
async def test_feedback_no_ctx():
    robin = Robin()
    res = await robin._feedback(msg='Dit is een teststring')
    assert res == 'context not spedified'


@pytest.mark.asyncio
async def test_feedback_delete_failed():
    robin = Robin()
    ctx = AsyncMock()
    ctx.message.delete.side_effect = Exception('Boom!')
    res = await robin._feedback(ctx=ctx, msg='Dit is een teststring', delete_message=True)
    assert res == 'message deletion failed Boom!'


@pytest.mark.asyncio
async def test_feedback_delete_message_success():
    robin = Robin()
    ctx = AsyncMock()
    res = await robin._feedback(ctx=ctx, msg='Dit is een teststring', delete_message=7)
    assert res == "Invallid option for delete_message 7"


@pytest.mark.asyncio
async def test_feedback_delete_message_fail():
    robin = Robin()
    ctx = AsyncMock()
    res = await robin._feedback(ctx=ctx, msg='Dit is een teststring', delete_message=True)
    assert res == 'feedback sent successful'


@pytest.mark.asyncio
async def test_feedback_delete():
    robin = Robin()
    ctx = AsyncMock()
    res = await robin._feedback(ctx=ctx, msg='Dit is een teststring', delete_after=4)
    assert res == 'feedback sent successful'


def test_usermap():
    robin = Robin()
    robin.conn = sqlite3.connect('tests/hades-test.db')
    res = robin._getusermap(1)
    assert res['discordid'] == 'discordid1'
