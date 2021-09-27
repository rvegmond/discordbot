from discord.ext import commands, tasks
from datetime import datetime
from loguru import logger
import os

from ..robin import Robin
from ..utils import feedback, normalize_time, rolemembers


class Comeback(Robin):
    """
    The class that contains the Comeback functions
    """

    def __init__(self, bot=None, db=None):
        super().__init__(bot=bot, db=db)
        self.return_scheduler.start()
        logger.info(f"Class {type(self).__name__} initialized ")

    ###############################################################################################
    #  command _update_comeback_channel
    ###############################################################################################

    async def _update_comeback_channel(self, comeback_channel, which_ws):
        bot = self.bot

        get_comback = (
            self.db.session.query(
                self.db.User.DiscordAlias,
                self.db.WSComeback.UserId,
                self.db.WSComeback.WSId,
                self.db.WSComeback.ShipType,
                self.db.WSComeback.ReturnTime,
                self.db.WSComeback.NotificationTime,
            )
            .filter(self.db.WSComeback.NotificationTime > datetime.now())
            .filter(self.db.WSComeback.WSId == which_ws)
            .join(self.db.User)
        )

        await comeback_channel.purge(limit=100)
        msg = (
            "In dit kanaal komt het overzicht wanneer je schip weer de ws in mag, dit kanaal is "
            f"specifiek voor {which_ws}. Met **`{bot.command_prefix}terug <schip> <terugkomtijd>`**"
            " geef je aan wanneer je schip weer terug de ws in mag. Het schip kan zijn *bs*, "
            "*ukkie* of *drone*. Voor de terugkomtijd kun je in twee formaten weergeven:\n"
            " **uu:mm**  - dit geeft de tijd vanaf nu, dit is voor een ukkie of een bs of\n"
            " **uu.t**   - dit is de tijd waarin t tienden van een uur zijn, dit is voor drones.\n"
            "Het is ook om een notificatietijd mee te geven, dit is dan de derde parameter. "
            "Dit is de tijd op de klok wanneer je de notificatie wilt ontvangen. Als je deze niet "
            "meegeeft krijg je en notifiatie op het moment dat je schip de ws weer in mag. "
            "Notificatietijd is in UU:MM, Robin houdt rekening met de dagwissel. Het commando is:\n"
            f" **`{bot.command_prefix}terug <schip> <terugkomtijd> <notificatietid>`**, bv.:\n"
            f"`{bot.command_prefix}terug bs 17:00 8:00` - ik kan over 17 uur vanaf nu weer een bs "
            "insturen maar wil morgen om 8:00 pas een notificatie."
            "\u2063"
        )

        await comeback_channel.send(msg)
        msg = "**Speler     Schip     TerugTijd     NotificatieTijd**\n"
        if get_comback.count() > 0:
            for item in get_comback.all():
                returntime = item.ReturnTime.strftime("%a %H:%M")
                notificationtime = item.NotificationTime.strftime("%a %H:%M")
                msg += f"**{item.DiscordAlias}**      {item.ShipType}         {returntime}       {notificationtime}\n"
        await comeback_channel.send(msg)

    ###############################################################################################
    #  command terug
    ###############################################################################################

    @commands.command(
        name="terug",
        help=(
            "Als je een schip verloren bent krijg je hiermee een seintje als je er weer in mag, "
            "dit is ook erg handig voor je mede spelers en de planners.\n"
            "!terug <schip> terugkomtijd  notificatietijd\n"
            "schiptype: bs of ukkie of drone\n"
            "tijdnotatie (zowel terugkom als notificatietijd):\n"
            " - XX:YY   uren, minuten worden bij huidige tijd geteld (bij verlies van een schip)\n"
            " - XX:YYu is de tijd op de klok, is voor de notificatietijd, corrigeert voor de dag\n"
            " - XX.Y    uren en 10en van uren, wordt omgerekend naar minuten (voor een drone)\n"
            "Zonder opgave van notificatietijd, krijg je ene notificatie op het moment van je "
            "terugkomtijd.\n"
        ),
        brief="Meld de terugkomtijd van je schip aan.",
    )
    async def terug(self, ctx, *args):
        comeback_channel = {}
        comeback_channel["ws1"] = self.bot.get_channel(
            int(os.getenv("WS1_COMEBACK_CHANNEL"))
        )
        comeback_channel["ws2"] = self.bot.get_channel(
            int(os.getenv("WS2_COMEBACK_CHANNEL"))
        )

        usermap = self._getusermap(int(ctx.author.id))
        returntime = normalize_time(args[1])
        logger.info(f"len(args) {len(args)}")
        logger.info(f"args {args}")
        if len(args) == 2:
            notificationtime = returntime
        elif len(args) == 3:
            notificationtime = normalize_time(args[2])
        else:
            # send help!
            await ctx.send_help(ctx.command)
            return None

        shiptype = args[0].lower()
        if shiptype in ["bs", "ukkie", "drone"]:
            result = (
                self.db.session.query(self.db.WSComeback)
                .filter(
                    self.db.WSComeback.UserId == usermap["UserId"],
                    self.db.WSComeback.ShipType == shiptype,
                )
                .count()
            )
            logger.info(f"count: {result}")
            if result > 0:
                self.db.session.query(self.db.WSComeback).filter(
                    self.db.WSComeback.UserId == usermap["UserId"],
                    self.db.WSComeback.ShipType == shiptype,
                ).delete()
        else:
            # wrong shiptype, send help!
            await ctx.send_help(ctx.command)
            return None

        ws = None
        for wslist in ["ws1", "ws2"]:
            if usermap["UserId"] in rolemembers(ctx=ctx, role_name=wslist):
                ws = wslist
        new_return = self.db.WSComeback(
            UserId=usermap["UserId"],
            WSId=ws,
            ShipType=shiptype,
            ReturnTime=datetime.strptime(returntime, "%Y-%m-%d %H:%M"),
            NotificationTime=datetime.strptime(notificationtime, "%Y-%m-%d %H:%M"),
        )
        self.db.session.add(new_return)
        self.db.session.commit()

        await self._update_comeback_channel(comeback_channel[ws], ws)
        if shiptype == "drone":
            await feedback(
                ctx,
                msg=(
                    f"{usermap['DiscordAlias']}, succes met ophalen van "
                    "relics, straks snel weer een nieuwe drone"
                ),
                delete_after=3,
                delete_message=True,
            )
        else:
            await feedback(
                ctx,
                msg=(
                    f"Helaas, {usermap['DiscordAlias']}, hopelijk volgende "
                    f"keer meer succes met je {shiptype}"
                ),
                delete_after=3,
                delete_message=True,
            )

    ###############################################################################################
    #  runner return_scheduler
    ###############################################################################################
    @tasks.loop(minutes=1)
    async def return_scheduler(self):
        """
        this is the "cron" for the comeback notifications
        """
        ws_channel = {}
        ws_channel["ws1"] = self.bot.get_channel(int(os.getenv("WS1_CHANNEL")))
        ws_channel["ws2"] = self.bot.get_channel(int(os.getenv("WS2_CHANNEL")))
        comeback_channel = {}
        comeback_channel["ws1"] = self.bot.get_channel(
            int(os.getenv("WS1_COMEBACK_CHANNEL"))
        )
        comeback_channel["ws2"] = self.bot.get_channel(
            int(os.getenv("WS2_COMEBACK_CHANNEL"))
        )
        to_notify = self.db.session.query(
            self.db.WSComeback.UserId,
            self.db.WSComeback.WSId,
            self.db.WSComeback.ShipType,
            self.db.WSComeback.ReturnTime,
            self.db.WSComeback.NotificationTime,
        ).filter(
            self.db.WSComeback.NotificationTime
            == datetime.strptime(
                datetime.now().strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M"
            )
        )
        if to_notify.count() > 0:
            for item in to_notify.all():
                await ws_channel[item.WSId].send(
                    f"<@{item.UserId}>, je {item.ShipType} mag de ws in, succes!"
                )
                await self._update_comeback_channel(
                    comeback_channel[item.WSId], item.WSId
                )
