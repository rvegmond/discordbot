import discord
import os
# import signal
from datetime import datetime
from discord.ext import commands
from loguru import logger
# from utils import generate_table

class Status(commands.Cog):
    def __init__(self, bot, conn):
        self.bot = bot
        self.conn = conn

    @commands.command(
        name="status",
        help=("Met het status commando update je status in het status kanaal,"
        " hiermee help je je mede ws-ers op de hoogte te houden hoe snel je kunt reageren."),        
        brief="Commando om je status in het status kanaal",
        )
    async def status(self, ctx, *args):
        conn = self.conn
        bot = self.bot
        status_channel = int(os.getenv("STATUS_CHANNEL"))
        cur = conn.cursor()
        query = f"delete from status where Naam = '{ctx.author.name}'"
        try:
            await ctx.message.delete()
        except Exception as e: 
            logger.info(f"message deletion failed {e}")
        try:
            cur.execute(query)
        except:
            logger.info(f"{ctx.author.name} doesn't have an entry in status yet..")
        now = datetime.now().strftime("%d-%m-%Y")
        query = f"insert into status values(?, ?, ?)"
        logger.info(query)
        cur.execute(query, [ctx.author.name, now, ' '.join(args)])
        conn.commit()
        channel = bot.get_channel(status_channel)
        logger.info(f"channel {channel}")

        query = """
                select g.Naam, 
                    case when s.LastUpdate is null then "0-0-000" else s.LastUpdate end, 
                    case when s.StatusText is null then "Geen status ingevuld" else s.StatusText end 
                from gsheet_v g
                left join status s
                on s.Naam = g.Naam 
                where lower(g.WhiteStar)=?
                order by lower(g.Naam)
                """
        async for message in channel.history(limit=200):
            await message.delete()
        for i in ("ws1","ws2"):
            logger.info(f"whitestar {i}")
            msg = ''
            cur.execute(query, [i])
            col1 = 15
            col2 = 15
            col3 = 35
            msg += "**{upper(i)}:**\n"
            msg += "**{row[0]}** - {row[1]} - {row[2]}\n" 
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


        logger.info("{}".format(ctx.author))  
        logger.info("status received")
        # await ctx.send(args)
        conn.commit()
