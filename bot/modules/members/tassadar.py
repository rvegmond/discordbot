"""
The contents of this file is to reflect happyness of robin.
"""
from discord.ext import commands
from ..robin import Robin
from ..utils import feedback


class Tassadar(Robin):
    """
    Are you happy Tassadar?
    """

    @commands.command(
        name="tassadar",
        help="Hoe is het met tassadar?",
        brief="Hoe is het met tassadar?",
    )
    async def command(self, ctx):
        """
        How are you Tass?
        """
        await feedback(ctx, msg="(https://www.youtube.com/watch?v=rBDwUXi1Sbw)")
