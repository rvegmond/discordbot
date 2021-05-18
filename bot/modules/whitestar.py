"""
All related to whitestar functionality
"""
import locale
import os
import datetime
from datetime import timedelta
from discord.ext import commands, tasks
from loguru import logger
from .robin import Robin, _sanitize
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
    def __init__(self, bot, conn=None):
        self.bot = bot
        self.conn = conn
        self.return_scheduler.start()
        logger.info(f"Class {type(self).__name__} initialized ")

###################################################################################################
#  command status
###################################################################################################

    async def update_status_table(self, ctx):
        """
        updating status table in status channel
        """
        conn = self.conn
        bot = self.bot
        status_channel = int(os.getenv("STATUS_CHANNEL"))
        channel = bot.get_channel(status_channel)
        await channel.purge(limit=100)
        msg = (
            "In dit kanaal staat een overzicht hoe snel de verwachte reactietijd van je mede ws "
            "teamgenoten is Je update je beschikbaarheid status met "
            f"**`{bot.command_prefix}status <bereikbaarheid>`**\n"
            "Houdt je bericht duidelijk, kort en bondig (max 100 tekens)\n"
        )
        msg += u"\u2063"
        await channel.send(msg)
        for this_ws in ("ws1", "ws2"):
            msg = f"**{this_ws.upper()}**\n"

            cur.execute("delete from temp_ws ")

            query = "insert into temp_ws (Id) values (?) "
            memberlist = _rolemembers(ctx=ctx, role_name=this_ws)
            for member in memberlist:
                cur.execute(query, [member])

            query = (
                "select um.DiscordAlias, "
                "case when s.LastUpdate is null then '01-01-1970 00:00:00' else s.LastUpdate end, "
                "case when s.StatusText is null then 'Geen status ingevuld' else s.StatusText end "
                "from temp_ws tw "
                "left join UserMap um "
                "on um.Id=tw.Id "
                "left join Status s "
                "on s.Id=um.Id "
            )

            try:
                cur.execute(query)
                for row in cur.fetchall():
                    yesterday = datetime.datetime.now() - timedelta(hours=36)
                    weekago = datetime.datetime.now() - timedelta(days=5)
                    user = row[0]
                    try:
                        lastupdate = datetime.datetime.strptime(row[1], '%d-%m-%Y %H:%M:%S')
                    except Exception as e:
                        logger.info(f"Exception: {e}")
                        lastupdate = datetime.datetime.strptime(row[1], '%d-%m-%Y')
                    status = row[2]
                    logger.info(f"lastupdate: {lastupdate}")
                    logger.info(f"yesterday: {yesterday}")
                    nicedate = lastupdate.strftime("%a %d/%m %H:%M")
                    if lastupdate < weekago:
                        msg += f"~~{user} - {nicedate} - {status}~~\n"
                    elif lastupdate <= yesterday:
                        msg += f"{user} - {nicedate} - {status}\n"
                    else:
                        msg += f"**{user} - {nicedate} - {status}**\n"

                msg += u"\u2063"
            except Exception as e:
                logger.info(f"error: {e}")
                return None
            conn.commit()
            await channel.send(msg)

###################################################################################################
#  command status
###################################################################################################

    @commands.command(
        name="status",
        help=("Met het status commando update je status in het status kanaal,"
              " hiermee help je je mede ws-ers op de hoogte te houden hoe snel je kunt reageren."
              ),
        brief="Update je status in het status kanaal",
    )
    async def status(self, ctx, *args):
        conn = self.conn
        bot = self.bot

        usermap = self._getusermap(int(ctx.author.id))
        statusupdate = _sanitize(' '.join(args), 100)
        cur = conn.cursor()
        logger.info(f"New status from {usermap['discordalias']}: {statusupdate} ")
        query = f"delete from status where Id='{usermap['Id']}' "
        try:
            cur.execute(query)
        except Exception as e:
            logger.info(f"{usermap['discordalias']} doesn't have a previous status set..")
            return None

        now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        query = "insert into status (Id, LastUpdate, StatusText) values (?, ?, ?) "
        cur.execute(query, [usermap['Id'], now, statusupdate])
        conn.commit()
        self.update_status_table(ctx)

        await ctx.send(
            content=f"Dank, {usermap['discordalias']} je ws-status is nu bijgewerkt",
            delete_after=3
        )

        try:
            await ctx.message.delete()
        except Exception as e:
            logger.info(f"message deletion failed {e}")
        conn.commit()

###################################################################################################
#  function update_ws_inschrijvingen_tabel
###################################################################################################

    async def update_ws_inschrijvingen_tabel(self, wslist_channel):
        """
        This wil write the list of "inschrijvingen" to the wslist_channel,
        it is based on the contents of the sqlite table
        """
        conn = self.conn
        bot = self.bot
        cur = conn.cursor()

        # Get all subscribers for the ws
        query = (
            "select um.DiscordAlias, w.inschrijving, w.Opmerkingen "
            "from WSinschrijvingen w "
            "left join UserMap um "
            "on w.Id = um.Id "
            "where actueel = 'ja' "
            "order by Inschrijving asc, Inschrijftijd asc "
        )
        cur.execute(query)
        msg = ''
        i = 1
        for row in cur.fetchall():
            if row[1] == 'planner':
                msg += f"**{i}. {row[0]} {row[1]} {row[2]}**\n"
            else:
                msg += f"{i}. {row[0]} {row[1]} {row[2]}\n"
            i += 1
        msg += "\n"

        # get number of planners
        query = (
            "select * "
            "from WSinschrijvingen w "
            "where w.actueel = 'ja' "
            "and w.inschrijving = 'planner' "
        )
        cur.execute(query)
        num_planners = len(cur.fetchall())

        # get number of players
        query = (
            "select * "
            "from WSinschrijvingen w "
            "where w.actueel = 'ja' "
            "and w.inschrijving = 'speler' "
        )
        cur.execute(query)
        num_players = len(cur.fetchall())

        msg += (
            f"**Planners:** {num_planners}, ",
            f"**Spelers:** {num_players}, ",
            f"**Totaal:** {num_planners+num_players}"
        )
        msg += "\n"

        async for message in wslist_channel.history(limit=20):
            if message.author == bot.user:
                await message.delete()
        await wslist_channel.send(msg)

###################################################################################################
#  command ws  (inschrijvingen)
###################################################################################################

    @commands.command(
        name="ws",
        help=(
            f"Met het ws commando schrijf je je in (of uit) voor de volgende ws, opties:\n"
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
            " clear - schoon het ws-inschrijvingen kanaal, inschrijvingen worden geopend.\n"),
        brief="Schrijf jezelf in voor de volgende ws",
    )
    async def ws(self, ctx, *args):
        """
        The function to handle the ws inschrijvingen related stuff
        TODO refactor, rename and simplify
        """
        conn = self.conn
        bot = self.bot
        usermap = self._getusermap(str(ctx.author.id))
        cur = conn.cursor()
        wsin_channel_id = int(os.getenv("WSIN_CHANNEL"))
        wsin_channel = bot.get_channel(int(os.getenv("WSIN_CHANNEL")))
        wslist_channel = bot.get_channel(int(os.getenv("WSLIST_CHANNEL")))
        ws_role = ctx.guild.get_role(int(os.getenv("WS_ROLE")))
        comment = ''

        if ctx.channel != wsin_channel:
            """ Trying to post in the wrong channel """
            await ctx.send(content=(
                f"{usermap['discordalias']}, je kunt alleen in kanaal <#{wsin_channel_id}> "
                "inschrijven, je bent nu nog **niet** ingeschreven!"), delete_after=5)
            try:
                await ctx.message.delete()
            except Exception as e:
                logger.info(f"message deletion failed {e}")
            return None

        if len(args) == 0:
            """ no arguments """
            # send help!
            await ctx.send_help(ctx.command)
            return None

        if len(args) > 1:
            """ more than 1 argument """
            comment = _sanitize(' '.join(args[1:]))

        if args[0] in ['i', 'in']:
            action = 'speler'
        elif args[0] in ['u', 'uit', 'o', 'out']:
            action = 'out'
            query = (
                "select * from WSinschrijvingen where Id=? and actueel='ja' "
            )
            cur.execute(query, [usermap['Id']])
            if len(cur.fetchall()) == 0:
                await ctx.send(
                    content=f"{usermap['discordalias']}, je stond nog niet ingeschreven.. ",
                    delete_after=3
                )
            else:
                query = (
                    "delete from WSinschrijvingen "
                    "where Id=? "
                    "and actueel='ja' "
                )

                cur.execute(query, [usermap['Id']])
                conn.commit()
                await ctx.send(
                    content=f"Helaas, {usermap['discordalias']} je doet niet mee met komende ws",
                    delete_after=1
                )
                await self.update_ws_inschrijvingen_tabel(wslist_channel)

                async for message in wsin_channel.history(limit=50):
                    if message.author.id == ctx.author.id:
                        try:
                            await message.delete()
                        except Exception as error:
                            logger.info(f"historic message deletion failed {error}")
                return None

        elif args[0] in ['p', 'plan', 'planner']:
            action = 'planner'
        elif args[0] in ['close', 'sluit']:
            if (await Roles.in_role(self, ctx, 'Moderator') or await Roles.in_role(self, ctx, 'Bot Bouwers')):

                await wsin_channel.set_permissions(ws_role, send_messages=False)
                await ctx.send(content=f"Inschrijving gesloten door {ctx.author.name}")
                return None
        elif args[0] in ['open']:
            if await Roles.in_role(self, ctx, 'Moderator') or await Roles.in_role(self, ctx, 'Bot Bouwers'):
                await wsin_channel.set_permissions(ws_role, send_messages=True)
                await ctx.send(content=f"Inschrijving geopend door {ctx.author.name}")
                return None
        elif args[0] in ['clear']:
            if await Roles.in_role(self, ctx, 'Moderator') or await Roles.in_role(self, ctx, 'Bot Bouwers'):
                msg = (
                    f"{ws_role.mention}, De WS inschrijving is geopend\n"
                    "Met `!ws plan` of `!ws p` schrijf je je in als planner en speler\n"
                    "Met `!ws in` of `!ws i` schrijf je je in als speler\n"
                    f"Inschrijven kan alleen in {wsin_channel.mention}, het overzicht van de "
                    f"inschrijvingen komt in {wslist_channel.mention}, met 30 inschrijvingen "
                    "worden er 2 wsen gestart, op voorwaarde van minimaal **4 planners** zijn."
                    "\n"
                    "Elke __**Dinsdag**__ worden de inschrijvingen geopend "
                    "ongeacht of er nog wssen lopen tot uiterlijk __**Woensdag**__")
                await wsin_channel.purge(limit=100)
                await wslist_channel.purge(limit=100)
                await wsin_channel.set_permissions(ws_role, send_messages=True)
                await ctx.send(content=msg)
                query = (
                    "update WSinschrijvingen "
                    "set actueel='nee' "
                )
                cur.execute(query)
                conn.commit()
                await self.update_ws_inschrijvingen_tabel(wslist_channel)
                return None
        else:
            await ctx.send("Ongeldige input")
            await ctx.send_help(ctx.command)
            return None

        # is member already registered
        query = (
            "select * from WSinschrijvingen where Id=? and inschrijving=? and actueel='ja' "
        )

        cur.execute(query, [usermap['Id'], action])
        rows_same_role = len(cur.fetchall())

        query = (
            "select * from WSinschrijvingen where Id=? and inschrijving <> ? and actueel='ja' "
        )

        cur.execute(query, [usermap['Id'], action])
        rows_different_role = len(cur.fetchall())

        if rows_same_role == 1:
            # already registerd with the same role, do nothing..
            await ctx.send(f"{usermap['discordalias']} is al ingeschreven als {action}")
            return None
        elif rows_different_role == 1:
            # already registerd as a different role, update
            query = (
                "update WSinschrijvingen set inschrijving=?, Opmerkingen=? "
                "where Id=? and actueel='ja' "
            )
            cur.execute(query, [action, comment, usermap['Id']])
            conn.commit()
            await ctx.send(
                content=f"Gefeliciteerd, {usermap['discordalias']} je bent nu {action} voor de volgende ws",
                delete_after=3
            )
        else:
            # not yet registerd, insert
            query = (
                "insert into WSinschrijvingen (Id, inschrijving, Inschrijftijd, Opmerkingen, actueel) "
                "values (?, ?, datetime('now'), ?, 'ja') "
            )
            cur.execute(query, [usermap['Id'], action, comment])
            conn.commit()
            await ctx.send(
                content=f"Gefeliciteerd, {usermap['discordalias']} je bent nu {action} voor de volgende ws",
                delete_after=3
            )
        await self.update_ws_inschrijvingen_tabel(wslist_channel)

###################################################################################################
#  command updateusermap
###################################################################################################

    @commands.command(
        name="updateusermap",
        help=(
            "Moderator only:\n"
            " geen argumenten, update de usermap tabel\n"),
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
        if await Roles.in_role(self, ctx, 'Moderator') or await Roles.in_role(self, ctx, 'Bot Bouwers'):
            conn = self.conn
            cur = conn.cursor()

            guild = ctx.guild
            members = guild.members
            select_query = "select * from usermap where Id=? "
            for member in members:
                cur.execute(select_query, [member.id])
                if len(cur.fetchall()) == 0:
                    logger.info(f"updated {member.display_name}")
                    query = "insert into usermap (Id, DiscordAlias) values (?, ?) "
                    cur.execute(query, [member.id, member.display_name])
            conn.commit()
            await ctx.send(f"usermap updated by {ctx.author.name}")

###################################################################################################
#  command _update_comeback_channel
###################################################################################################

    async def _update_comeback_channel(self, comeback_channel, ws):
        conn = self.conn
        bot = self.bot
        cur = conn.cursor()
        query = (
            "select um.DiscordAlias, ShipType, ReturnTime, NotificationTime "
            "from WSReturn w "
            "left join UserMap um "
            "on um.Id  = w.Id "
            "where w.NotificationTime > STRFTIME('%Y-%m-%d %H:%M', datetime('now', 'localtime')) "
            "and w.ws = ? "
        )
        cur.execute(query, [ws])
        result = cur.fetchall()
        await comeback_channel.purge(limit=100)
        msg = (
            f"In dit kanaal komt het overzicht wanneer je schip weer de ws in mag, dit kanaal is "
            f"specifiek voor {ws}. Met **`{bot.command_prefix}terug <schip> <terugkomtijd>`** geef "
            "je aan wanneer je schip weer terug de ws in mag. Het schip kan zijn *bs*, *ukkie* of "
            "*drone*. Voor de terugkomtijd kun je in twee formaten weergeven:\n"
            " **uu:mm**  - dit geeft de tijd vanaf nu, dit is voor een ukkie of een bs of\n"
            " **uu.t**   - dit is de tijd waarin t tienden van een uur zijn, dit is voor drones.\n"
            "Het is ook om een notificatietijd mee te geven, dit is dan de derde parameter. "
            "Dit is de tijd op de klok wanneer je de notificatie wilt ontvangen. Als je deze niet "
            "meegeeft krijg je en notifiatie op het moment dat je schip de ws weer in mag. "
            "Notificatietijd is in UU:MM, Robin houdt rekening met de dagwissel. Het commando is:\n"
            f" **`{bot.command_prefix}terug <schip> <terugkomtijd> <notificatietid>`**, bv.:\n"
            f"`{bot.command_prefix}terug bs 17:00 8:00` - ik kan over 17 uur vanaf nu weer een bs "
            "insturen maar wil morgen om 8:00 pas een notificatie."
            u"\u2063"
            "**Speler     Schip     TerugTijd     NotificatieTijd**\n"
        )

        if len(result) > 0:
            for row in result:
                returntime = _normalize_time(row[2]).strftime("%a %H:%M")
                notificationtime = _normalize_time(row[3]).strftime("%a %H:%M")
                msg += f"**{row[0]}**      {row[1]}          {returntime}       {notificationtime}\n"
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
            "terugkomtijd.\n"),
        brief="Meld de terugkomtijd van je schip aan.",
    )
    async def terug(self, ctx, *args):
        conn = self.conn
        comeback_channel = {}
        comeback_channel['ws1'] = self.bot.get_channel(int(os.getenv('WS1_COMEBACK_CHANNEL')))
        comeback_channel['ws2'] = self.bot.get_channel(int(os.getenv('WS2_COMEBACK_CHANNEL')))

        usermap = self._getusermap(int(ctx.author.id))
        cur = conn.cursor()
        returntime = _normalize_time(args[1])

        if len(args) == 2:
            notificationtime = _normalize_time(args[1])
        elif len(args) == 3:
            now = datetime.datetime.now()
            intime = args[2]
            (hours, minutes) = intime.split(':')
            intime = datetime.datetime(now.year, now.month, now.day, int(hours), int(minutes), 0)
            if intime < now:
                intime = intime + datetime.timedelta(days=1)
            notificationtime = _normalize_time(intime)
        else:
            # send help!
            await ctx.send_help(ctx.command)
            return None

        shiptype = args[0].lower()
        if shiptype in ['bs', 'ukkie', 'drone']:
            query = "select * from  WSReturn where Id=? and Shiptype=?"
            cur.execute(query, [usermap['Id'], shiptype])
            if len(cur.fetchall()) > 0:
                query = "delete from WSReturn where Id=? and Shiptype=?"
                cur.execute(query, [usermap['Id'], shiptype])
        else:
            # wrong shiptype, send help!
            await ctx.send_help(ctx.command)
            return None

        ws = None
        for wslist in ['ws1', 'ws2']:
            if usermap['Id'] in _rolemembers(ctx=ctx, role_name=wslist):
                ws = wslist
        try:
            query = (
                "insert into WSReturn (Id, WS, Shiptype, ReturnTime, NotificationTime) "
                "values (?, ?, ?, ?, ?) ")
            cur.execute(query, [usermap['Id'], ws, shiptype, returntime, notificationtime])
            conn.commit()
        except Exception as e:
            logger.info(f"insert failed {e}: __{' '.join(args)}")
            await ctx.send_help(ctx.command)

        await self._update_comeback_channel(comeback_channel[ws], ws)
        if shiptype == 'drone':
            await self._feedback(
                ctx,
                msg=(
                    f"{usermap['discordalias']}, succes met ophalen van "
                    "relics, straks snel weer een nieuwe drone"
                ),
                delete_after=3,
                delete_message=True
            )
        else:
            await self._feedback(
                ctx,
                msg=(
                    f"Helaas, {usermap['discordalias']}, hopelijk volgende "
                    "keer meer succes met je {shiptype}"
                ),
                delete_after=3,
                delete_message=True
            )

    @tasks.loop(minutes=1)
    async def return_scheduler(self):
        conn = self.conn
        ws_channel = {}
        ws_channel['ws1'] = self.bot.get_channel(int(os.getenv('WS1_CHANNEL')))
        ws_channel['ws2'] = self.bot.get_channel(int(os.getenv('WS2_CHANNEL')))
        comeback_channel = {}
        comeback_channel['ws1'] = self.bot.get_channel(int(os.getenv('WS1_COMEBACK_CHANNEL')))
        comeback_channel['ws2'] = self.bot.get_channel(int(os.getenv('WS2_COMEBACK_CHANNEL')))
        cur = conn.cursor()
        query = (
            "select Id, ws, ShipType, ReturnTime, NotificationTime "
            "from WSReturn w "
            "where w.NotificationTime=STRFTIME('%Y-%m-%d %H:%M', datetime('now', 'localtime'))"
        )
        cur.execute(query)
        result = cur.fetchall()
        if len(result) > 0:
            for row in result:
                await ws_channel[row[1]].send(f"<@{row[0]}>, je {row[2]} mag weer de ws in, succes!")
                await self._update_comeback_channel(comeback_channel[row[1]], row[1])

    def dummy(self, ctx):
        conn = self.conn
        query = (
            "select Id "
            "from WSReturn "
        )
        cur = conn.cursor()
        cur.execute(query)
        msg = []
        result = cur.fetchall()
        for row in result:
            msg += f"{row[0]}\n"
        return result


###################################################################################################
#  _normalize_time
###################################################################################################

def _normalize_time(intime: str
                    ) -> str:
    """
    Translate the intime to a normal "clock" time.
    The input can be hours from now, clock time or hours + hours/10

    paramters:
        intime:     The time to normalize
    Output:
        intime:     The normalized time
    """
    now = datetime.datetime.now()
    if '.' in intime or ',' in intime:
        logger.info(f"found . {intime}")
        (hours, minutes) = intime.split('.')
        intime = now + datetime.timedelta(hours=int(hours), minutes=int(minutes) * 6)
        intime = intime.strftime("%Y-%m-%d %H:%M")
    elif ':' in intime:
        logger.info(f"found : {intime}")
        (hours, minutes) = intime.split(':')
        intime = now + datetime.timedelta(hours=int(hours), minutes=int(minutes))
        intime = intime.strftime("%Y-%m-%d %H:%M")
    logger.info(f"return{intime}")
    return intime
