import discord
import os
# import signal
from datetime import datetime
from discord.ext import commands
from loguru import logger
# from utils import generate_table

class WhiteStar(commands.Cog):
    def __init__(self, bot, conn):
        self.bot = bot
        self.conn = conn

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
        cur = conn.cursor()
        DiscordId = str(ctx.author)
        logger.info(f"New status from {DiscordId}: {' '.join(args)} ")

        query = f"delete from status where DiscordId = '{DiscordId}'"
        try:
            await ctx.message.delete()
        except Exception as e: 
            logger.info(f"message deletion failed {e}")
        try:
            cur.execute(query)
        except:
            logger.info(f"{DiscordId} doesn't have a previous status set..")
        query = f"select * from UserMap where DiscordId=?"
        logger.info(query)
        cur.execute(query, [DiscordId])
        rowcount = len(cur.fetchall())
        logger.info(f"rowcount {rowcount}")
        if rowcount == 0:
            query = f"insert into UserMap values (?, ?, ?)"
            logger.info(query)
            cur.execute(query, [DiscordId, ctx.author.name, ctx.author.name])     
        now = datetime.now().strftime("%d-%m-%Y")
        query = f"insert into status values(?, ?, ?)"
        logger.info(query)
        cur.execute(query, [DiscordId, now, ' '.join(args)])
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
