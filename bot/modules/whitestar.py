import discord
import os
# import signal
from datetime import datetime
from discord.ext import commands
from loguru import logger
from .robin import Robin
from .roles import Roles



class WhiteStar(Robin):
######################################################################################################
#  command status
######################################################################################################

    @commands.command(
        name="status",
        help=("Met het status commando update je status in het status kanaal,"
        " hiermee help je je mede ws-ers op de hoogte te houden hoe snel je kunt reageren."),        
        brief="Update je status in het status kanaal",
        )
    async def status(self, ctx, *args):
        conn = self.conn
        bot = self.bot

        status_channel = int(os.getenv("STATUS_CHANNEL"))
        channel = bot.get_channel(status_channel)
        usermap = self._getusermap(int(ctx.author.id))  
        statusupdate = self._sanitize(' '.join(args), 100)
        cur = conn.cursor()
        logger.info(f"New status from {usermap['discordalias']}: {statusupdate} ")
        query = f"delete from status where Id = '{usermap['Id']}'"
        try:
            cur.execute(query)
        except:
            logger.info(f"{usermap['discordalias']} doesn't have a previous status set..")
            return None
     
        now = datetime.now().strftime("%d-%m-%Y")
        query = f"insert into status (Id, LastUpdate, StatusText) values (?, ?, ?)"
        cur.execute(query, [usermap['Id'], now, statusupdate])
        conn.commit()

        await channel.purge(limit=100)
        msg = ''        
        for i in ("ws1", "ws2"):
            l = []
            msg += f"**{i.upper()}**\n" 

            cur.execute("delete from temp_ws")

            query = "insert into temp_ws (Id) values (?)"
            memberlist = self._rolemembers(ctx, i)
            for member in memberlist:
                cur.execute(query, [member])

            query = """
                    select um.DiscordAlias, 
                        case when s.LastUpdate is null then "0-0-000" else s.LastUpdate end, 
                        case when s.StatusText is null then "Geen status ingevuld" else s.StatusText end 
                    from temp_ws tw
                    left join UserMap um
                    on um.Id = tw.Id 
                    left join Status s
                    on s.Id = um.Id
                    """
            try:
                cur.execute(query)
                for row in cur.fetchall():
                    msg += f"**{row[0]}** - {row[1]} - {row[2]}\n" 
                msg += "\n"
            except Exception as e:
                logger.info(f"error: {e}")
                pass
            conn.commit()
        await channel.send(msg) 
        await ctx.send(content=f"Dank, {usermap['discordalias']} je ws-status is nu bijgewerkt", delete_after=3)

        try:
            await ctx.message.delete()
        except Exception as e: 
            logger.info(f"message deletion failed {e}")
        conn.commit()

######################################################################################################
#  function update_ws_inschrijvingen_tabel
######################################################################################################

    async def update_ws_inschrijvingen_tabel(self, ctx, wslist_channel):
        conn = self.conn
        bot = self.bot
        cur = conn.cursor()

        # Get all subscribers for the ws
        query = """
                select um.DiscordAlias, w.inschrijving, w.Opmerkingen
                from WSinschrijvingen w 
                left join UserMap um 
                on w.Id = um.Id
                where actueel = 'ja'
                order by Inschrijving desc, Inschrijftijd asc
                """
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
        query = """
                select *
                from WSinschrijvingen w 
                where w.actueel = 'ja'
                and w.inschrijving = 'plan'
                """
        cur.execute(query)
        num_planners = len(cur.fetchall())

        # get number of players
        query = """
                select *
                from WSinschrijvingen w 
                where w.actueel = 'ja'
                and w.inschrijving = 'in'
                """
        # async for message in channel.history(limit=2):
        #     await message.delete()
        cur.execute(query)
        num_players = len(cur.fetchall())

        msg += f"**Planners:** {num_planners}, **Spelers:** {num_players}, **Totaal:** {num_planners+num_players}"
        msg += "\n"

        async for message in wslist_channel.history(limit=20):
            if message.author == bot.user:  
                await message.delete()  
        await wslist_channel.send(msg)




######################################################################################################
#  command ws  (inschrijvingen)
######################################################################################################

    @commands.command(
        name="ws",
        help=("Met het ws commando schrijf je je in (of uit) voor de volgende ws, opties:\n"
        " plan/p [opmerking] - aanmelden als planner voor de volgende ws\n"
        " in/i [opmerking]   - aanmelden als speler voor de volgende ws\n"
        " uit/u              - afmelden voor de volgende ws (als je aangemeld was)\n"
        "\n"
        "Moderator only:\n"
        " open  - open het ws-inschrijvingen kanaal\n"
        " close - sluit het ws-inschrijvingen kanaal\n"
        " clear - schoon het ws-inschrijvingen kanaal, inschrijvingen worden geopend.\n"),
        brief="Schrijf jezelf in voor de volgende ws",
        # hidden="True",
        )
    async def ws(self, ctx, *args):
        conn = self.conn
        bot = self.bot
        usermap = self._getusermap(str(ctx.author.id))
        cur = conn.cursor()
        # query = """
        # select * from WSstatus
        # """
        # cur.execute(query)
        # ws_status = cur.fetchone()
        wsin_channel_id = int(os.getenv("WSIN_CHANNEL"))
        wsin_channel = bot.get_channel(int(os.getenv("WSIN_CHANNEL")))
        wslist_channel = bot.get_channel(int(os.getenv("WSLIST_CHANNEL")))


        if ctx.channel != wsin_channel:
            await ctx.send(content=f"{usermap['discordalias']}, je kunt alleen in kanaal <#{wsin_channel_id}> inschrijven, je bent nu nog **niet** ingeschreven!", delete_after=5)
            try:
                await ctx.message.delete()
            except Exception as e: 
                logger.info(f"message deletion failed {e}")
            return None
        else:
            comment = ''
            if len(args) == 0:
                # send help!
                await ctx.send_help(ctx.command)
                return None
            elif len(args) > 1:
                # there is a comment
                comment = self.sanitize(' '.join(args[1:]))
            
            if args[0] in ['i', 'in']:
                action = 'speler'
            elif args[0] in ['u', 'uit', 'o', 'out']:
                action = 'out'
                query = """
                        select * from WSinschrijvingen where Id = ? and actueel = 'ja'
                        """
                cur.execute(query, [usermap['Id']])
                if len(cur.fetchall()) == 0:
                    await ctx.send(content=f"{usermap['discordalias']}, je stond nog niet ingeschreven voor de volgende ws", delete_after=3)
                else:
                    query = """
                            delete from WSinschrijvingen 
                            where Id=?
                            and actueel = 'ja'
                            """
                    # logger.info(f"query {query}, Id: {usermap['Id']}")

                    cur.execute(query, [usermap['Id']])
                    conn.commit()
                    await ctx.send(content=f"Helaas, {usermap['discordalias']} je doet niet meer mee met de volgende ws", delete_after=1)
                    await self.update_ws_inschrijvingen_tabel(ctx, wslist_channel)

                    async for message in wsin_channel.history(limit=50):
                        # await ctx.send(content=f"messageauthor.id: {message.author.id}, ctx {ctx.author.id}")
                        if message.author.id == ctx.author.id:  
                            try:
                                await message.delete()
                            except Exception as e: 
                                logger.info(f"historic message deletion failed {e}")
                    return None
 
            elif args[0] in ['p', 'plan', 'planner']:
                action = 'planner'
            elif args[0] in ['close', 'sluit']:
                if await Roles.in_role(self, ctx, 'Moderator'):
                    await wsin_channel.set_permissions(ctx.guild.default_role, send_messages=False)
                    await ctx.send(content=f"Inschrijving gesloten door {ctx.author.name}")
                    return None
            elif args[0] in ['open' ]:
                if await Roles.in_role(self, ctx, 'Moderator'):
                    await wsin_channel.set_permissions(ctx.guild.default_role, send_messages=True)
                    await ctx.send(content=f"Inschrijving geopend door {ctx.author.name}")
                    return None
            elif args[0] in ['clear']:
                if await Roles.in_role(self, ctx, 'Moderator'):
                    await wsin_channel.purge(limit=100)
                    await wsin_channel.set_permissions(ctx.guild.default_role, send_messages=True)
                    await ctx.send(content=f"Inschrijving geopend door {ctx.author.name}")
                    query = """
                            update WSinschrijvingen 
                            set actueel = 'nee'
                            """
                    cur.execute(query)
                    conn.commit()
                    await self.update_ws_inschrijvingen_tabel(ctx, wslist_channel)
                    return None
            # elif args[0] in ['info']:
            #     await ctx.send(content=f"Current WS is {ws_status[0]}, delete_after=3")

            else:
                await ctx.send("Ongeldige input")
                await ctx.send_help(ctx.command)
                return None

            # is member already registered
            query = """
                    select * from WSinschrijvingen where Id = ? and inschrijving = ? and actueel = 'ja'
                    """

            cur.execute(query, [usermap['Id'], action])
            rows_same_role = len(cur.fetchall())

            query = """
                    select * from WSinschrijvingen where Id = ? and inschrijving <> ? and actueel = 'ja'
                    """

            cur.execute(query, [usermap['Id'], action])
            rows_different_role = len(cur.fetchall())

            if rows_same_role == 1:
                # already registerd with the same role, do nothing..
                await ctx.send(f"{usermap['discordalias']} is al ingeschreven als {action}")
                return None
            elif rows_different_role == 1:
                # already registerd as a different role, update
                query = """
                        update WSinschrijvingen set inschrijving=?, Opmerkingen=?
                        where Id = ? and actueel = 'ja'
                        """
                cur.execute(query, [action, comment, usermap['Id']])
                conn.commit()
                await ctx.send(content=f"Gefeliciteerd, {usermap['discordalias']} je bent nu {action} voor de volgende ws", delete_after=3)
            else:
                # not yet registerd, insert
                query = """
                        insert into WSinschrijvingen (Id, inschrijving, Inschrijftijd, Opmerkingen, actueel)
                        values (?, ?, datetime('now'), ?, 'ja')
                        """
                cur.execute(query, [usermap['Id'], action, comment])
                conn.commit()
                await ctx.send(content=f"Gefeliciteerd, {usermap['discordalias']} je bent nu {action} voor de volgende ws", delete_after=3)
        await self.update_ws_inschrijvingen_tabel(ctx, wslist_channel)

    @commands.command()
    async def updateusermap(self, ctx, *args):
        """
        Get the mapping for discordalias and gsheetalias
        Id is the key for the selection.
        If Id is not yet in usermap table it will be added 
        with the provided alias.
        """
        if await Roles.in_role(self, ctx, 'Moderator'):
            conn = self.conn
            usermap = {}
            cur = conn.cursor()

            guild = ctx.guild
            members = guild.members
            select_query = "select * from usermap where Id=?"
            for member in members:
                cur.execute(select_query, [member.Id])
                if len(cur.fetchall()) == 0:
                    query = "insert into usermap (Id, DiscordAlias) values (?, ?)"
                    cur.execute(query, [member.id, member.display_name ])
                else:
                    pass
            conn.commit()
            await ctx.send(f"usermap updated by {ctx.author.name}")
        else:
            pass
 



