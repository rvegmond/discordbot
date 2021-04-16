import discord
from discord.ext import commands
from loguru import logger
import sqlite3
import sys

from modules import whitestar, ping, roles

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
        logger.info(f"connected successful to {db_file}")
    except Exception as e: 
        logger.info(f"connection failed {e}")
        sys.exit(3)

    return conn



def new_bot(command_prefix: str, description: str) -> discord.ext.commands.bot:
    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix=command_prefix, description=description, intents=intents)
    conn = create_connection(db_file) 

    @bot.event
    async def on_ready():
        logger.info(f"Signed in as [{bot.user.id}] [{bot.user.name}]")
        
        bot.add_cog(ping.Ping(bot))
        bot.add_cog(whitestar.WhiteStar(bot, conn))
        bot.add_cog(roles.Roles(bot, conn))


    return bot
