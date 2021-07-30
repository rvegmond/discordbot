"""
these tests should cover functions and classes in robin.py
"""
import pytest
from mock import AsyncMock, patch
from bot.modules.utils import feedback

TESTSTRING = "Dit is een teststring"
SUCCESSFUL_FEEDBACK = "feedback sent successful"


@pytest.mark.asyncio
async def testfeedback():
    """
    These tests will check feedback result when everything is fine.
    """
    context = AsyncMock()
    res = await feedback(ctx=context, msg=TESTSTRING)
    assert res == SUCCESSFUL_FEEDBACK


@pytest.mark.asyncio
async def testfeedback_no_ctx():
    """
    These tests will check feedback result when contexts is nog spedified
    """
    res = await feedback(msg=TESTSTRING)
    assert res == "context not spedified"


@pytest.mark.asyncio
async def testfeedback_delete_failed():
    """
    These tests will check feedback result when deletion of msg failed.
    """
    context = AsyncMock()
    context.message.delete.side_effect = Exception("Boom!")
    res = await feedback(ctx=context, msg=TESTSTRING, delete_message=True)
    assert res == "message deletion failed Boom!"


@pytest.mark.asyncio
async def testfeedback_delete_message_wrong_argument():
    """
    These tests will check feedback result when wrong argument is specified.
    """
    context = AsyncMock()
    res = await feedback(ctx=context, msg=TESTSTRING, delete_message=7)
    assert res == "Invallid option for delete_message 7"


@pytest.mark.asyncio
async def testfeedback_delete_message_fail():
    """
    These tests will check feedback result when deletion of msg succeeds.
    """
    context = AsyncMock()
    res = await feedback(ctx=context, msg=TESTSTRING, delete_message=True)
    assert res == SUCCESSFUL_FEEDBACK


@pytest.mark.asyncio
async def testfeedback_delete():
    """
    These tests will check feedback result when deletion of msg succeeds.
    """
    context = AsyncMock()
    res = await feedback(ctx=context, msg=TESTSTRING, delete_after=4)
    assert res == SUCCESSFUL_FEEDBACK
