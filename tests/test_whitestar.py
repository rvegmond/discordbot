# """
# these tests should cover functions and classes in robin.py
# """
# import datetime
# import pytest
# import sqlite3
# from mock import AsyncMock, MagicMock
# from bot.modules.whitestar import WhiteStar, _normalize_time

# bot = MagicMock()

# whitestar = WhiteStar(bot)
# # whitestar.conn = sqlite3.connect('tests/hades-test.db')


# # @pytest.mark.asyncio
# # async def test_status():
# #     """
# #     check to see normalized time in "dot" time from now
# #     """
# #     ctx = AsyncMock()
# #     whitestar.update_status_table = AsyncMock()
# #     ctx.author.id = 1
# #     await whitestar.status(ctx, 'nieuwe status')
# #     cur = whitestar.conn.cursor()
# #     res = cur.execute("select StatusText from status")
# #     assert res.fetchone()[0] == 'nieuwe status'

# # def test_dummy():
# #     """
# #     Dummy test to experiment with testing.
# #     """
# #
# #     result = [['John', 'Bill']]
# #     whitestar.conn = MagicMock()
# #     ctx = MagicMock()
# #     whitestar.conn = MagicMock()
# #     whitestar.conn.cursor().fetchall.return_value = result
# #     res = whitestar.dummy(ctx)
# #     assert res == 'John'
