from discord.ext import commands
from loguru import logger
from datetime import datetime, timedelta
import os

from ..robin import Robin
from ..utils import feedback, normalize_time, sanitize, rolemembers


class Status(Robin):
    """
    The class that contains the Comeback functions
    """

    ###############################################################################################
    #  command update_status_table
    ###############################################################################################

    async def update_status_table(self, ctx):
        """
        updating status table in status channel
        """
        bot = self.bot
        status_channel = int(os.getenv("STATUS_CHANNEL"))
        channel = bot.get_channel(status_channel)
        yesterday = datetime.now() - timedelta(hours=36)
        weekago = datetime.now() - timedelta(days=5)
        await channel.purge(limit=100)
        msg = (
            "In dit kanaal staat een overzicht hoe snel de verwachte reactietijd van je mede ws "
            "teamgenoten is Je update je beschikbaarheid status met "
            f"**`{bot.command_prefix}status <bereikbaarheid>`**\n"
            "Houdt je bericht duidelijk, kort en bondig (max 100 tekens)\n"
        )
        msg += "\u2063"
        await channel.send(msg)
        for this_ws in ("ws1", "ws2"):
            msg = f"**{this_ws.upper()}**\n"

            self.db.session.query(self.db.WSTemp).delete()

            memberlist = rolemembers(ctx=ctx, role_name=this_ws)
            for member in memberlist:
                new_tmp = self.db.WSTemp(UserId=member)
                self.db.session.add(new_tmp)

            get_status = (
                self.db.session.query(
                    self.db.User.DiscordAlias,
                    self.db.Status.LastUpdate,
                    self.db.Status.StatusText,
                )
                .join(self.db.WSTemp)
                .join(self.db.Status)
            )
            for item in get_status.all():
                nice_last_update = item.LastUpdate.strftime("%a %d/%m %H:%M")
                if item.LastUpdate < weekago:
                    msg += f"~~{item.DiscordAlias} - {nice_last_update} - {item.StatusText}~~\n"
                elif item.LastUpdate <= yesterday:
                    msg += f"{item.DiscordAlias} - {nice_last_update} - {item.StatusText}\n"
                else:
                    msg += f"**{item.DiscordAlias} - {nice_last_update} - {item.StatusText}**\n"

                msg += "\u2063"
            await channel.send(msg)
        self.db.session.commit()

    ###############################################################################################
    #  command status
    ###############################################################################################

    @commands.command(
        name="status",
        help=(
            "Met het status commando update je status in het status kanaal,"
            " hiermee help je je mede ws-ers op de hoogte te houden hoe snel je kunt reageren."
        ),
        brief="Update je status in het status kanaal",
    )
    async def status(self, ctx, *args):
        """
        updating the status of ws participants
        """

        usermap = self._getusermap(int(ctx.author.id))
        statusupdate = sanitize(" ".join(args), 100)

        logger.info(f"New status from {usermap['DiscordAlias']}: {statusupdate} ")
        self.db.session.query(self.db.Status).filter(
            self.db.Status.UserId == usermap["UserId"]
        ).delete()

        new_status = self.db.Status(UserId=usermap["UserId"], StatusText=statusupdate)
        self.db.session.add(new_status)

        await self.update_status_table(ctx)

        await ctx.send(
            content=f"Dank, {usermap['DiscordAlias']} je ws-status is nu bijgewerkt",
            delete_after=3,
        )

        try:
            await ctx.message.delete()
        except Exception as exception:
            logger.info(f"message deletion failed {exception}")
        self.db.session.commit()
