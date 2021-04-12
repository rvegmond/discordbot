import discord
import os
# import signal
from datetime import datetime
from discord.ext import commands
from loguru import logger
from .robin import Robin

class WhiteStar(Robin):

    @commands.command(
        name="status",
        help=("Met het status commando update je status in het status kanaal,"
        " hiermee help je je mede ws-ers op de hoogte te houden hoe snel je kunt reageren."),        
        brief="Hiermee update je je status in het status kanaal",
        )
    async def status(self, ctx, *args):
        conn = self.conn
        bot = self.bot
        status_channel = int(os.getenv("STATUS_CHANNEL"))
        UserMap = self.getUserMap(str(ctx.author), str(ctx.author.name))  
        statusupdate = self.sanitize(' '.join(args), 100)
        cur = conn.cursor()
        logger.info(f"New status from {UserMap['DiscordId']}: {statusupdate} ")

        query = f"delete from status where DiscordId = '{UserMap['DiscordId']}'"
        try:
            await ctx.message.delete()
        except Exception as e: 
            logger.info(f"message deletion failed {e}")
        try:
            cur.execute(query)
        except:
            logger.info(f"{UserMap['DiscordId']} doesn't have a previous status set..")

     
        now = datetime.now().strftime("%d-%m-%Y")
        query = f"insert into status values(?, ?, ?)"
        logger.info(query)
        cur.execute(query, [UserMap['DiscordId'], now, statusupdate])
        conn.commit()
        channel = bot.get_channel(status_channel)
        logger.info(f"channel {channel}")

        query = """
                select case when um.DiscordAlias is null then '.'||g.Naam else um.DiscordAlias end, 
                    case when s.LastUpdate is null then "0-0-000" else s.LastUpdate end, 
                    case when s.StatusText is null then "Geen status ingevuld" else s.StatusText end 
                from gsheet_v g
                left join UserMap um 
                on g.Naam = um.GsheetAlias 
                left join status s
                on um.DiscordId = s.DiscordId 
                where g.WhiteStar = ?
                order by lower(g.Naam)
                """
        async for message in channel.history(limit=200):
            await message.delete()
        msg = ''        
        for i in ("ws1","ws2"):
            logger.info(f"whitestar {i}")
            cur.execute(query, [i])
            # col1 = 15
            # col2 = 15
            # col3 = 35
            msg += f"**{i.upper()}:**\n"
            for row in cur.fetchall():
                msg += f"**{row[0]}** - {row[1]} - {row[2]}\n" 
            msg += "\n"

            # msg += '-' * (col1 + col2 + col3 + 4)

            # msg = "```\n"
            # msg += '-' * (col1 + col2 + col3 + 4)
            # msg += '\n'
            # msg += f"|{i.upper().center(col1 + col2 + col3 + 2, ' ')}|\n"
            # msg += '-' * (col1 + col2 + col3 + 4)
            # msg += '\n'
            # msg += f"|{'User'.center(col1, ' ')}|{'Last Update'.center(col2, ' ')}|{'Status'.center(col3, ' ')}|\n"
            # msg += '-' * (col1 + col2 + col3 + 4)
            # msg += '\n'
            # for row in cur.fetchall():
            #     msg += f"|{row[0].center(col1, ' ')}|{row[1].center(col2, ' ')}|{row[2].ljust(col3, ' ')}|\n" 
            # msg += '-' * (col1 + col2 + col3 + 4)
            # msg += "```"
        await channel.send(msg) 

        conn.commit()
