from discord.ext import commands
from loguru import logger
from datetime import datetime, timedelta
import os

from ..robin import Robin
from ..utils import feedback, normalize_time, sanitize, rolemembers


class Idee(Robin):
    """
    The class that contains the Comeback functions
    """

    ###############################################################################################
    #  command status
    ###############################################################################################

    @commands.command(
        name="idee",
        help=(
            "Met het status commando update je status in het status kanaal,"
            " hiermee help je je mede ws-ers op de hoogte te houden hoe snel je kunt reageren."
        ),
        brief="Update je status in het status kanaal",
    )
    async def idee(self, ctx, *args):
        """
        updating the status of ws participants
        """

        usermap = self._getusermap(int(ctx.author.id))
        idea = sanitize(" ".join(args), 100)
        if ctx.channel.id == int(os.getenv("WS1_CHANNEL")):
            officers_channel = self.bot.get_channel(
                int(os.getenv("WS1_OFFICERS_CHANNEL"))
            )
        elif ctx.channel.id == int(os.getenv("WS2_CHANNEL")):
            officers_channel = self.bot.get_channel(
                int(os.getenv("WS2_OFFICERS_CHANNEL"))
            )
        else:
            await ctx.send(
                content=f"{usermap['DiscordAlias']} post je idee in het ws-kanaal",
                delete_after=3,
            )
            return
        logger.info(f"New idea from {usermap['DiscordAlias']}: {idea} ")

        await ctx.send(
            content=f"Dank, {usermap['DiscordAlias']} je is doorgestuurd aan de officers",
            delete_after=3,
        )

        msg = f"idee van {usermap['DiscordAlias']}: {idea}"
        await officers_channel.send(msg)
