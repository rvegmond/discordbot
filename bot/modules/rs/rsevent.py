"""
The contents of this file is to reflect happyness of robin.
"""
from discord.ext import commands
from ..robin import Robin
from sqlalchemy import func
import os


class RSEvent(Robin):
    """
    Are you happy Robin?
    """

    async def update_rsevent_table(self, ctx):
        """
        updating status table in status channel
        """
        bot = self.bot
        eventlist_channel = int(os.getenv("EVENTLIST_CHANNEL"))
        channel = bot.get_channel(eventlist_channel)
        await channel.purge(limit=100)
        msg = (
            "semi real-time overzicht van het aantal rs-en welke iedereen"
            "gedaan heeft\n"
        )
        msg += "\u2063"
        get_status = (
            self.db.session.query(
                self.db.User.DiscordAlias, func.count("*").label("run_count")
            )
            .join(self.db.RSEvent, self.db.RSEvent.DiscordId == self.db.User.UserId)
            .group_by(self.db.User.DiscordAlias)
            .order_by(func.count("*").desc())
        )
        for item in get_status.all():
            msg += f"{item.DiscordAlias} - {item.run_count} \n"
        msg += "\u2063"
        await channel.send(msg)

    ###############################################################################################
    #  command status
    ###############################################################################################

    @commands.command(
        name="rsevent",
        help=(
            "Met het status commando update je status in het status kanaal,"
            " hiermee help je je mede ws-ers op de hoogte te houden hoe snel je kunt reageren."
        ),
        brief="Update je status in het status kanaal",
    )
    async def command(self, ctx, *args):
        """
        updating the status of ws participants
        """

        await self.update_rsevent_table(ctx)
