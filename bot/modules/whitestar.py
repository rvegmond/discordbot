"""
All related to whitestar functionality
"""
import locale
import os
import datetime
from datetime import timedelta, datetime
from discord.ext import commands, tasks
from loguru import logger
from .robin import Robin, _sanitize, _feedback
from .roles import Roles, _rolemembers

try:
    locale.setlocale(locale.LC_ALL, "nl_NL.utf8")  # required running on linux
    logger.info("running on linux")
except locale.Error:
    locale.setlocale(locale.LC_ALL, "nl_NL.UTF-8")  # required when running on MAC
    logger.info("running on mac")


class WhiteStar(Robin):
    """
    The class that contains the Whitestar functions
    """

    def __init__(self, bot=None, db=None):
        super().__init__(bot=bot, db=db)
        self.return_scheduler.start()
        logger.info(f"Class {type(self).__name__} initialized ")

    ###################################################################################################
    #  command status
    ###################################################################################################

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

            memberlist = _rolemembers(ctx=ctx, role_name=this_ws)
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

    ###################################################################################################
    #  command status
    ###################################################################################################

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
        statusupdate = _sanitize(" ".join(args), 100)

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

    ###################################################################################################
    #  function update_ws_inschrijvingen_tabel
    ###################################################################################################

    async def update_ws_inschrijvingen_tabel(self, wslist_channel):
        """
        This wil write the list of "inschrijvingen" to the wslist_channel,
        it is based on the contents of the sqlite table
        """
        bot = self.bot

        # Get all subscribers for the ws
        get_entries = (
            self.db.session.query(
                self.db.WSEntry.EntryType,
                self.db.WSEntry.Remark,
                self.db.User.DiscordAlias,
            )
            .filter_by(Active=True)
            .join(self.db.User)
            .order_by(self.db.WSEntry.EntryType)
            .order_by(self.db.WSEntry.EntryTime)
        )
        msg = ""
        i = 1
        for item in get_entries.all():
            logger.info(f"item {item}")
            if item.EntryType == "planner":
                msg += f"**{i}. {item.DiscordAlias} {item.EntryType} {item.Remark}**\n"
            else:
                msg += f"{i} {item.DiscordAlias} {item.EntryType} {item.Remark}\n"
            i += 1
        msg += "\n"
        num_planners = (
            self.db.session.query(self.db.WSEntry)
            .filter_by(Active=True)
            .filter_by(EntryType="planner")
            .count()
        )
        num_players = (
            self.db.session.query(self.db.WSEntry)
            .filter_by(Active=True)
            .filter_by(EntryType="speler")
            .count()
        )

        logger.info(f"num_players: {num_players}, num_planners: {num_planners}")
        msg += (
            f"**Planners:** {num_planners}, "
            f"**Spelers:** {num_players}, "
            f"**Totaal:** {num_planners+num_players}"
        )
        msg += "\n"

        async for message in wslist_channel.history(limit=20):
            if message.author == bot.user:
                logger.debug(
                    f"going to delete message for {message.author} == {bot.user}"
                )
                await message.delete()
        await wslist_channel.send(msg)

    ###################################################################################################
    #  function _ws_entry
    ###################################################################################################

    async def _ws_entry(
        self, ctx: commands.Context = None, action: str = "", comment: str = ""
    ):
        """
        Handle the entry for the ws
        """
        bot = self.bot

        usermap = self._getusermap(str(ctx.author.id))
        wsin_channel = bot.get_channel(int(os.getenv("WSIN_CHANNEL")))
        wslist_channel = bot.get_channel(int(os.getenv("WSLIST_CHANNEL")))

        is_entered = (
            self.db.session.query(self.db.WSEntry)
            .filter_by(Active=True)
            .filter_by(UserId=usermap["UserId"])
            .count()
        )
        logger.info(f"is_entered: {is_entered}")
        logger.info(f"{usermap['DiscordAlias']} heeft als action: {action}")
        if action == "out":
            if is_entered == 0:
                logger.info(f"{usermap['DiscordAlias']} stond nog niet ingeschreven.. ")
                msg = f"{usermap['DiscordAlias']}, je stond nog niet ingeschreven.. "
                await _feedback(ctx=ctx, msg=msg, delete_after=3)
            else:
                self.db.session.query(self.db.WSEntry).filter_by(Active=True).filter_by(
                    UserId=usermap["UserId"]
                ).delete()
                logger.info(f"{usermap['DiscordAlias']} stond wel ingeschreven.. ")
                msg = (
                    f"Helaas, {usermap['DiscordAlias']} je doet niet mee met komende ws"
                )
                await _feedback(ctx=ctx, msg=msg, delete_after=3)

                await self.update_ws_inschrijvingen_tabel(wslist_channel)

                async for message in wsin_channel.history(limit=50):
                    if message.author.id == ctx.author.id:
                        logger.info(f"deleting message for {message.author.id}")
                        await message.delete()
            return None
        rows_same_role = (
            self.db.session.query(self.db.WSEntry)
            .filter_by(Active=True)
            .filter_by(UserId=usermap["UserId"])
            .filter_by(EntryType=action)
            .count()
        )
        logger.info(f"rows_same_role {rows_same_role}")
        if rows_same_role == 1:
            # already registerd with the same role, do nothing..
            await ctx.send(f"{usermap['DiscordAlias']} is al ingeschreven als {action}")
            return None
        if is_entered == 1:
            logger.info(f"updating")
            # already registerd as a different role, update
            data = {"EntryType": action, "Remark": comment}
            self.db.session.query(self.db.WSEntry).filter_by(Active=True).filter_by(
                UserId=usermap["UserId"]
            ).update(data)
        else:
            logger.info(f"adding")
            # not yet registerd, insert
            new_entry = self.db.WSEntry(
                UserId=usermap["UserId"], EntryType=action, Remark=comment, Active=True
            )
            self.db.session.add(new_entry)
        await ctx.send(
            content=(
                f"Gefeliciteerd, {usermap['DiscordAlias']} "
                f"je bent nu {action} voor de volgende ws"
            ),
            delete_after=3,
        )
        self.db.session.commit()

    ###################################################################################################
    #  function _ws_admin
    ###################################################################################################

    async def _ws_admin(self, ctx, action: str):
        """
        execute administrative tasks for the WS entry
        """
        bot = self.bot
        wsin_channel = bot.get_channel(int(os.getenv("WSIN_CHANNEL")))
        wslist_channel = bot.get_channel(int(os.getenv("WSLIST_CHANNEL")))
        ws_role = ctx.guild.get_role(int(os.getenv("WS_ROLE")))

        # close
        if not (
            await Roles.in_role(self, ctx, "Moderator")
            or await Roles.in_role(self, ctx, "Bot Bouwers")
        ):
            await _feedback(
                ctx=ctx, msg="You are not an admin", delete_after=5, delete_message=True
            )
            return None

        if action == "open":
            await wsin_channel.set_permissions(ws_role, send_messages=True)
            # await wslist_channel.set_permissions(ws_role, send_messages=True)
            await ctx.send(content=f"Inschrijving geopend door {ctx.author.name}")
        elif action == "close":
            await wsin_channel.set_permissions(ws_role, send_messages=False)
            await wslist_channel.set_permissions(ws_role, send_messages=False)
            await ctx.send(content=f"Inschrijving gesloten door {ctx.author.name}")
        elif action == "clear":
            msg = (
                f"{ws_role.mention}, De WS inschrijving is geopend\n"
                "Met `!ws plan` of `!ws p` schrijf je je in als planner en speler\n"
                "Met `!ws in` of `!ws i` schrijf je je in als speler\n"
                f"Inschrijven kan alleen in {wsin_channel.mention}, het overzicht van de "
                f"inschrijvingen komt in {wslist_channel.mention}, met 30 inschrijvingen "
                "worden er 2 wsen gestart, op voorwaarde van minimaal **4 planners** zijn."
                "\n"
                "Elke __**Dinsdag**__ worden de inschrijvingen geopend "
                "ongeacht of er nog wssen lopen tot uiterlijk __**Woensdag**__"
            )
            await wsin_channel.purge(limit=100)
            await wslist_channel.purge(limit=100)
            await ctx.send(content=msg)
            data = {"Active": False}
            self.db.session.query(self.db.WSEntry).update(data)
            await self.update_ws_inschrijvingen_tabel(wslist_channel)
            await wsin_channel.set_permissions(ws_role, send_messages=True)
            self.db.session.commit()
            return None

    ###################################################################################################
    #  command ws  (inschrijvingen)
    ###################################################################################################

    @commands.command(
        name="ws",
        help=(
            "Met het ws commando schrijf je je in (of uit) voor de volgende ws, opties:\n"
            " plan/p [opmerking] - aanmelden als planner voor de volgende ws\n"
            " in/i [opmerking]   - aanmelden als speler voor de volgende ws\n"
            " uit/u              - afmelden voor de volgende ws (als je aangemeld was)\n"
            "\n"
            "\n"
            "Inschrijven kan **alleen** in het #ws-inschrijvingen kanaal. Het overzicht komt in "
            "#ws-inschrijflijst. Updaten van je rol (speler -> planner) kan door je in te "
            "schrijven met je nieuwe rol.\n"
            "inschrijven planner met !ws plan\n"
            "inschrijven als speler met !ws in\n"
            "uitschrijven kan met !ws out\n"
            "\n"
            "Onderstaande opties zijn voor Moderator only:\n"
            " open  - open het ws-inschrijvingen kanaal\n"
            " close - sluit het ws-inschrijvingen kanaal\n"
            " clear - schoon het ws-inschrijvingen kanaal, inschrijvingen worden geopend.\n"
        ),
        brief="Schrijf jezelf in voor de volgende ws",
    )
    async def ws(self, ctx, *args):
        """
        The function to handle the ws inschrijvingen related stuff
        """
        usermap = self._getusermap(str(ctx.author.id))
        wsin_channel_id = int(os.getenv("WSIN_CHANNEL"))
        wsin_channel = self.bot.get_channel(int(os.getenv("WSIN_CHANNEL")))
        wslist_channel = self.bot.get_channel(int(os.getenv("WSLIST_CHANNEL")))
        comment = ""

        if ctx.channel != wsin_channel:
            # Trying to post in the wrong channel
            msg = (
                f"{usermap['DiscordAlias']}, je kunt alleen in kanaal <#{wsin_channel_id}> "
                "inschrijven, je bent nu nog **niet** ingeschreven!"
            )

            await _feedback(ctx=ctx, msg=msg, delete_after=3, delete_message=True)
            return None
        if len(args) == 0:
            # no arguments, send help!
            await ctx.send_help(ctx.command)
            return None

        if len(args) > 1:
            # more than 1 argument, join
            comment = _sanitize(" ".join(args[1:]))

        logger.info(f"{usermap['DiscordAlias']} - {args[0]} - {comment}")
        if args[0] in ["i", "in"]:
            await self._ws_entry(ctx, action="speler", comment=comment)
        elif args[0] in ["p", "plan", "planner"]:
            await self._ws_entry(ctx, action="planner", comment=comment)
        elif args[0] in ["u", "uit", "o", "out"]:
            await self._ws_entry(ctx, action="out", comment=comment)
        elif args[0] in ["close", "sluit"]:
            await self._ws_admin(ctx, action="close")
        elif args[0] in ["open"]:
            await self._ws_admin(ctx, action="open")
        elif args[0] in ["clear"]:
            await self._ws_admin(ctx, action="clear")
        else:
            await ctx.send("Ongeldige input")
            await ctx.send_help(ctx.command)
            return None

        await self.update_ws_inschrijvingen_tabel(wslist_channel)

    ###################################################################################################
    #  command updateusermap
    ###################################################################################################

    @commands.command(
        name="updateusermap",
        help=("Moderator only:\n" " geen argumenten, update de usermap tabel\n"),
        brief="Update de usermap tabel",
        hidden="True",
    )
    async def updateusermap(self, ctx):
        """
        Get the mapping for discordalias and gsheetalias
        Id is the key for the selection.
        If Id is not yet in usermap table it will be added
        with the provided alias.
        """
        if await Roles.in_role(self, ctx, "Moderator") or await Roles.in_role(
            self, ctx, "Bot Bouwers"
        ):

            guild = ctx.guild
            members = guild.members

            for member in members:
                if (
                    self.db.session.query(self.db.User)
                    .filter_by(UserId=member.id)
                    .count()
                    == 0
                ):

                    new_user = self.db.User(
                        UserId=member.id, DiscordAlias=member.display_name
                    )
                    self.db.session.add(new_user)
                    self.db.session.commit()
                    logger.info(f"inserted {member.display_name}")

            await ctx.send(f"user table updated by {ctx.author.name}")

    ###################################################################################################
    #  command _update_comeback_channel
    ###################################################################################################

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
            .join(self.db.User)
            .filter_by(self.db.WSComeback.NotificationTime > datetime.now())
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

    ###################################################################################################
    #  command terug
    ###################################################################################################

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
        returntime = _normalize_time(args[1])

        if len(args) == 2:
            notificationtime = returntime
        elif len(args) == 3:
            notificationtime = _normalize_time(args[2])
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
            if usermap["UserId"] in _rolemembers(ctx=ctx, role_name=wslist):
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
            await _feedback(
                ctx,
                msg=(
                    f"{usermap['DiscordAlias']}, succes met ophalen van "
                    "relics, straks snel weer een nieuwe drone"
                ),
                delete_after=3,
                delete_message=True,
            )
        else:
            await _feedback(
                ctx,
                msg=(
                    f"Helaas, {usermap['DiscordAlias']}, hopelijk volgende "
                    f"keer meer succes met je {shiptype}"
                ),
                delete_after=3,
                delete_message=True,
            )

    ###################################################################################################
    #  command info
    ###################################################################################################

    @commands.command(
        name="info",
        help=("Geeft info over een een speler."),
        brief="Geeft info over een speler.",
    )
    async def info(self, ctx, *args):

        if len(args) != 1:
            await ctx.send_help(ctx.command)
            return None
        user = args[0]
        logger.info(f"user {user}")
        if (
            self.db.session.query(self.db.User).filter_by(DiscordAlias=user).count()
            == 0
        ):
            msg = f"User: {user} is onbekend."
        else:
            row = (
                self.db.session.query(self.db.User)
                .filter_by(DiscordAlias=user)
                .all()[0]
            )

            if row.LastActive is None:
                last_active = "Al even niet actief.."
                last_channel = "niet bekend"
            else:
                last_active = row.LastActive
                last_channel = row.LastChannel
            msg = (
                f"Info over: **{row.DiscordAlias}**\n\n"
                f"DiscordAlias: {row.DiscordAlias}\n"
                f"DiscordId: {row.UserId}\n"
                f"Laatst actief op discord: {last_active}\n"
                f"Laatst actief in kanaal: {last_channel}"
            )
        await _feedback(ctx=ctx, msg=msg)

    ###################################################################################################
    #  runner return_scheduler
    ###################################################################################################
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
        ).filter_by(
            NotificationTime=datetime.strptime(
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


###################################################################################################
#  _normalize_time
###################################################################################################


def _normalize_time(intime: str) -> str:
    """
    Translate the intime to a normal "clock" time.
    The input can be hours from now, clock time or hours + hours/10

    paramters:
        intime:     The time to normalize
    Output:
        intime:     The normalized time
    """
    logger.info(f"intime: {intime}")
    now = datetime.now()
    logger.info(f"now: {now}")
    if "." in intime or "," in intime:
        logger.info(f"found . {intime}")
        (hours, minutes) = intime.split(".")
        logger.info(f"hours: {hours}, minutes: {minutes}")
        intime = now + timedelta(hours=int(hours), minutes=int(minutes) * 6)
    elif "u" in intime:
        logger.info(f"found u {intime}")
        intime = intime.replace("u", "")
        (hours, minutes) = intime.split(":")
        intime = datetime.datetime(
            now.year, now.month, now.day, int(hours), int(minutes), 0
        )
        if intime < now:
            intime = intime + timedelta(days=1)
    elif ":" in intime:
        logger.info(f"found : {intime}")
        (hours, minutes) = intime.split(":")
        logger.info(f"hours: {hours}, minutes: {minutes}")
        intime = now + timedelta(hours=int(hours), minutes=int(minutes))
        logger.info(f"intime: {intime}")
    intime = intime.strftime("%Y-%m-%d %H:%M")
    logger.info(f"return {intime}")
    return intime
