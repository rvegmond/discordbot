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
        status_channel = int(os.getenv("STATUS_CHANNEL"))
        channel = bot.get_channel(status_channel)
        await channel.purge(limit=100)
        msg = (
            "Soort van real-time overzicht van het aantal rs-en welke iedereen"
            "gedaan heeft\n"
        )
        msg += "\u2063"
        await channel.send(msg)
        get_status = (
            self.db.session.query(self.db.User.DiscordAlias, func.count("*"))
            .join(self.db.RSQueue)
            .group_by(self.db.User.DiscordAlias)
        )
        for item in get_status.all():
            msg += f"{item.DiscordAlias} - {func.count('*')} \n"
        msg += "\u2063"
        await channel.send(msg)
