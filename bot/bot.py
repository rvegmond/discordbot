"""
The main file for the bot Robin.
"""
import sqlite3
import os
import sys
import discord
from discord.ext import commands
from loguru import logger
from datetime import datetime
from modules import whitestar, ping, roles

DB_FILE = "../data/hades.db"

___VERSION___ = "[v1.4.1]"

config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": ___VERSION___
            + " [{time:YYYY-MM-DD at HH:mm:ss}] [{level}]: {message}",
        }
    ],
}


def create_connection():
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        logger.info(f"connected successful to {DB_FILE}")
    except Exception as error:
        logger.info(f"connection failed {error}")
        sys.exit(3)

    return conn


def update_last_active(conn, message):
    cur = conn.cursor()
    member = message.author
    channel = message.channel

    if member.nick is None:
        membername = member.name
    else:
        membername = member.nick

    logger.info(f"member {member}")
    logger.info(f"member.id {member.id}")
    logger.info(f"membername {membername}")
    logger.info(f"channel.name {channel.name}")
    now = datetime.now()
    query = "select * from UserMap where Id=? "
    cur.execute(query, [member.id])
    row = cur.fetchone()
    if row is None:
        query = "insert into usermap (Id, DiscordAlias,last_active, last_channel) values (?, ?, ?, ?)"
        cur.execute(query, [member.id, membername, channel.name, now])
    else:
        query = "update usermap set DiscordAlias=?, last_active=?, last_channel=? where Id=? "
        cur.execute(query, [membername, now, channel.name, member.id])
    conn.commit()


def new_bot(command_prefix: str, description: str) -> discord.ext.commands.bot:
    """Create a new discordbot"""

    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(
        command_prefix=command_prefix, description=description, intents=intents
    )
    conn = create_connection()

    @bot.event
    async def on_message(message):
        logger.info(f"message {message}")
        update_last_active(conn, message)
        await bot.process_commands(message)

    @bot.event
    async def on_ready():
        logger.info(f"Signed in as [{bot.user.id}] [{bot.user.name}]")

        bot.add_cog(ping.Ping(bot))
        bot.add_cog(whitestar.WhiteStar(bot, conn))
        bot.add_cog(roles.Roles(bot, conn))

    return bot


if __name__ == "__main__":
    logger.configure(**config)
    logger.info("Now loading...")
    b = new_bot(
        command_prefix=os.getenv("COMMAND_PREFIX", "!"),
        description=os.getenv("BOT_DESCRIPTION", f"Robin, version {___VERSION___ }"),
    )
    b.run(os.getenv("DISCORD_TOKEN"))
