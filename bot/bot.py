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
from modules import whitestar, ping, roles, rs
import modules.db as db

db.session = db.init("sqlite:///../data/hades.db")
___VERSION___ = "[v2.0.0]"

config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": ___VERSION___
            + " [{time:YYYY-MM-DD at HH:mm:ss}] [{level}]: {message}",
        }
    ],
}


def update_rsruns(content):
    text = content.split()
    i = 0
    for item in text:
        print(f"{i} __{item}__")
        i += 1

    if len(text) > 1 and "start" in text[1]:
        logger.info(f"content {content}")
        level = text[0].replace("rs", "")
        logger.info(f"level {level}")
        for line in text[2:6]:
            if "<@" in line:
                user = line.replace("<@", "").replace(">", "")
                logger.info(f"user {user}")
                new_entry = db.RSEvent(DiscordId=user, RSLevel=level)
                db.session.add(new_entry)
#                await self.update_rsevent_table()



def update_last_active(message):
    member = message.author
    channel = message.channel

    if member.nick is None:
        membername = member.name
    else:
        membername = member.nick
    if member.name == "RedStarQueueBot":
        update_rsruns(message.content)
    logger.info(f"member {member}")
    logger.info(f"member.id {member.id}")
    logger.info(f"membername {membername}")
    logger.info(f"channel.name {channel.name}")
    if db.session.query(db.User).filter_by(UserId=member.id).count() == 0:
        new_user = db.User(
            UserId=member.id, DiscordAlias=membername, LastChannel=channel.name
        )
        db.session.add(new_user)
    else:
        data = {"DiscordAlias": membername, "LastChannel": channel.name}
        db.session.query(db.User).filter(db.User.UserId == member.id).update(data)

    db.session.commit()


def new_bot(command_prefix: str, description: str) -> discord.ext.commands.bot:
    """Create a new discordbot"""

    intents = discord.Intents.default()
    intents.members = True
    bot = commands.Bot(
        command_prefix=command_prefix, description=description, intents=intents
    )

    @bot.event
    async def on_message(message):
        logger.info(f"message {message}")
        update_last_active(message)
        await bot.process_commands(message)

    @bot.event
    async def on_ready():
        logger.info(f"Signed in as [{bot.user.id}] [{bot.user.name}]")

        bot.add_cog(ping.Ping(bot))
        bot.add_cog(whitestar.WhiteStar(bot=bot, db=db))
        bot.add_cog(roles.Roles(bot=bot, db=db))
        bot.add_cog(rs.RSEvent(bot=bot, db=db))

    return bot


if __name__ == "__main__":
    logger.configure(**config)
    logger.info("Now loading...")
    b = new_bot(
        command_prefix=os.getenv("COMMAND_PREFIX", "!"),
        description=os.getenv("BOT_DESCRIPTION", f"Robin, version {___VERSION___ }"),
    )
    b.run(os.getenv("DISCORD_TOKEN"))
