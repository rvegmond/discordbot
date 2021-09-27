"""
The contents of this file is to reflect happyness of robin.
"""
from discord.ext import commands
from ..robin import Robin
from ..utils import feedback


class Shamrock(Robin):
    """
    Are you happy Shamrock?
    """

    @commands.command(
        name="shamrock",
        help="Hoe is het met shamrock?",
        brief="Hoe is het met shamrock?",
    )
    async def command(self, ctx):
        """
        How are you Sham?
        """
        await feedback(
            ctx,
            msg="Voelt zich niet zo lekker,\n had gister dat laatste biertje niet moeten nemen...",
        )
