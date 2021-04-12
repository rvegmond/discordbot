import discord
from discord.ext import commands
from loguru import logger
import sqlite3

from modules import whitestar, ping

db_file = 'data/hades.db'

# logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def generate_table(msg):
    return msg
    
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except:
        logger.info("connection failed")

    return conn



def new_bot(command_prefix: str, description: str) -> discord.ext.commands.bot:
    bot = commands.Bot(command_prefix=command_prefix, description=description)
    conn = create_connection(db_file) 

    @bot.event
    async def on_ready():
        logger.info(f"Signed in as [{bot.user.id}] [{bot.user.name}]")
        
        bot.add_cog(ping.Ping(bot))
        bot.add_cog(whitestar.WhiteStar(bot, conn))


    return bot
