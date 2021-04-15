import discord
import os
# import signal
from datetime import datetime
from discord.ext import commands
from loguru import logger
from .robin import Robin
from .roles import Roles
from discord.utils import get



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
        usermap = self.getusermap(str(ctx.author), str(ctx.author.name))  
        statusupdate = self.sanitize(' '.join(args), 100)
        cur = conn.cursor()
        logger.info(f"New status from {usermap['discordid']}: {statusupdate} ")

        query = f"delete from status where discordid = '{usermap['discordid']}'"

        try:
            cur.execute(query)
        except:
            logger.info(f"{usermap['discordid']} doesn't have a previous status set..")
            return None

     
        now = datetime.now().strftime("%d-%m-%Y")
        query = f"insert into status values(?, ?, ?)"
        logger.info(query)
        cur.execute(query, [usermap['discordid'], now, statusupdate])
        conn.commit()

        logger.info(f"channel {channel}")
        
        # create temporary table.

        async for message in channel.history(limit=2):
            await message.delete()
        msg = ''        
        for i in ("ws1","ws2"):
            l = []
            msg += f"**{i.upper()}**\n" 
            query = "delete from temp_ws"
            cur.execute(query)
            query = "insert into temp_ws (username) values (?)"
            memberlist = await self.rolemembers(ctx, i)
            for member in memberlist:
                cur.execute(query, [member])
            query = """
                    select tw.username, 
                        case when s.LastUpdate is null then "0-0-000" else s.LastUpdate end, 
                        case when s.StatusText is null then "Geen status ingevuld" else s.StatusText end 
                    from temp_ws tw
                    left join UserMap um
                    on um.DiscordAlias = tw.username 
                    left join Status s
                    on s.DiscordId = um.DiscordId
                    """
            try:
                cur.execute(query)
                alle = cur.fetchall() 
                for row in alle:
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

    async def update_ws_inschrijvingen_tabel(self, ctx, wsq_channel):
        conn = self.conn
        cur = conn.cursor()

        # Get all subscribers for the ws
        query = """
                select um.DiscordAlias, w.inschrijving, w.Opmerkingen
                from WSinschrijvingen w 
                left join UserMap um 
                on w.DiscordId = um.DiscordId
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
                select count(1)
                from WSinschrijvingen w 
                where w.actueel = 'ja'
                and w.inschrijving = 'plan'
                group by w.inschrijving
                """
        cur.execute(query)
        num_planners = cur.fetchone()[0]

        # get number of players
        query = """
                select count(1)
                from WSinschrijvingen w 
                where w.actueel = 'ja'
                and w.inschrijving = 'in'
                group by w.inschrijving
                """
        # async for message in channel.history(limit=2):
        #     await message.delete()
        cur.execute(query)
        num_players = cur.fetchone()[0]

        msg += f"**Planners:** {num_planners}, **Spelers:** {num_players}, **Totaal:** {num_planners+num_players}"
        msg += "\n"

        async for message in wsq_channel.history(limit=2):
            # if message.author == bot.user:  
            await message.delete()  
        await wsq_channel.send(msg)

    async def rolemembers(self, ctx, *args): # Always same role, no input needed
        guild = ctx.guild
        role_name = args[0] 
        role_id = get(guild.roles, name=role_name)

        members = []
        x = role_id.members
        for t in x:
            members.append(t.name)
        return members

######################################################################################################
#  command ws  (inschrijvingen)
######################################################################################################

    @commands.command(
        name="ws",
        help=("Met het ws commando schrijf je je in (of uit) voor de volgende ws,"
        " 1e argument is in/i uit/u/out/o of plan, indien je uitschrijft schrijf je je helemaal uit."
        "    Bij een rol update (van speler naar planner) hoef je niet eerst jezelf eruit te gooien."
        " 2e argument is optioneel, is tekst input voor de ws samensteller (bv. casual)"),        
        brief="Schrijf jezelf in voor de volgende ws",
        hidden="True",
        )
    async def ws(self, ctx, *args):
        conn = self.conn
        bot = self.bot
        wsq_channel = bot.get_channel(int(os.getenv("WSQ_CHANNEL")))   
        cur = conn.cursor()
        usermap = self.getusermap(str(ctx.author), str(ctx.author))
        comment = ''
        if len(args) == 0:
            # send help!
            await ctx.send_help(ctx.command)
            return None
        elif len(args) > 1:
            # there is a comment
            comment = self.sanitize(' '.join(args))
        
        if args[0] in ['i', 'in']:
            action = 'speler'
        elif args[0] in ['u', 'uit', 'o', 'out']:
            action = 'out'
            query = """
                    select * from WSinschrijvingen where DiscordId = ? and actueel = 'ja'
                    """
            cur.execute(query, [usermap['discordid']])
            if len(cur.fetchall()) == 0:
                await ctx.send(content=f"{usermap['discordalias']}, je stond nog niet ingeschreven voor de volgende ws", delete_after=3)
            else:
                query = """
                        delete from WSinschrijvingen 
                        where DiscordId=?
                        and actueel = 'ja'
                        """
                logger.info(f"query {query}, discordid: {usermap['discordid']}")

                cur.execute(query, [usermap['discordid']])
                conn.commit()
                await ctx.send(content=f"Helaas, {usermap['discordalias']} je doet niet meer mee met de volgende ws", delete_after=3)
                await self.update_ws_inschrijvingen_tabel(ctx, wsq_channel)
            try:
                await ctx.message.delete()
            except Exception as e: 
                logger.info(f"message deletion failed {e}")
            return None
        elif args[0] in ['p', 'plan', 'planner']:
            action = 'planner'
        else:
            await ctx.send("Ongeldige input")
            await ctx.send_help(ctx.command)
            return None
        logger.info(f"usermap['discordid']: {usermap['discordid']}")  
        logger.info(f"comment: {comment}")  

        # is member already registered
        query = """
                select * from WSinschrijvingen where DiscordId = ? and inschrijving = ? and actueel = 'ja'
                """

        cur.execute(query, [usermap['discordid'], action])
        rows_same_role = len(cur.fetchall())

        query = """
                select * from WSinschrijvingen where DiscordId = ? and actueel = 'ja'
                """

        cur.execute(query, [usermap['discordid']])
        rows_different_role = len(cur.fetchall())


        if rows_same_role == 100:
            # already registerd with the same role, do nothing..
            await ctx.send(f"{usermap['DiscordAlias']} is al ingeschreven als {action}")
            return None
        elif rows_different_role == 1:
            # already registerd as a different role, update
            query = """
                    update WSinschrijvingen set inschrijving=?, Opmerkingen=?
                    where DiscordId = ? and actueel = 'ja'
                    """
            cur.execute(query, [action, comment, usermap['discordid']])
            conn.commit()
            try:
                await ctx.message.delete()
            except Exception as e: 
                logger.info(f"message deletion failed {e}")
            await ctx.send(content=f"Gefeliciteerd, {usermap['discordalias']} je bent nu {action} voor de volgende ws", delete_after=3)
        else:
            # not yet registerd, insert
            query = """
                    insert into WSinschrijvingen (DiscordId, inschrijving, Inschrijftijd, Opmerkingen, actueel)
                    values (?, ?, datetime('now'), ?, 'ja')
                    """
            cur.execute(query, [usermap['discordid'], action, comment])
            conn.commit()
            try:
                await ctx.message.delete()
            except Exception as e: 
                logger.info(f"message deletion failed {e}")
            await ctx.send(content=f"Gefeliciteerd, {usermap['discordalias']} je bent nu {action} voor de volgende ws", delete_after=3)
        await self.update_ws_inschrijvingen_tabel(ctx, wsq_channel)



 



