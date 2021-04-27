import sqlite3
import os
import sys
import discord
from discord.ext import commands
from loguru import logger
from modules import whitestar, ping, roles

DB_FILE = 'data/hades.db'

___VERSION___ = "[v1.1.0]"

config = {
    "handlers": [
        {"sink": sys.stdout,
         "format": ___VERSION___ + " [{time:YYYY-MM-DD at HH:mm:ss}] [{level}]: {message}"}
    ],
}


def generate_table(msg):
    return msg


def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        logger.info(f"connected successful to {DB_FILE}")
    except Exception as e:
        logger.info(f"connection failed {e}")
        sys.exit(3)

    return conn


def new_bot(command_prefix: str, description: str) -> discord.ext.commands.bot:
    """ Create a new discordbot
    """

    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(command_prefix=command_prefix, description=description, intents=intents)
    conn = create_connection()

    @bot.event
    async def on_ready():
        logger.info(f"Signed in as [{bot.user.id}] [{bot.user.name}]")

        # bot.add_cog(ping.Ping(bot))
        bot.add_cog(whitestar.WhiteStar(bot, conn))
        bot.add_cog(roles.Roles(bot, conn))
        # bot.add_cog(scheduler.Scheduler(bot, conn))
    return bot


if __name__ == "__main__":
    logger.configure(**config)
    logger.info("Now loading...")
    b = new_bot(command_prefix=os.getenv("COMMAND_PREFIX", "!"),
                description=os.getenv("BOT_DESCRIPTION", f"A discord bot, running version {___VERSION___ }"))
    b.run(os.getenv("DISCORD_TOKEN"))
