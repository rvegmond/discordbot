import discord
from discord.ext import commands
from loguru import logger


class Robin(commands.Cog):
    def __init__(self, bot, conn):
        self.bot = bot
        self.conn = conn
        logger.info(f"Class {type(self).__name__} initialized ")


    def getUserMap(self, DiscordId, Alias=None):
        """
        Get the mapping for DiscordAlias and GsheetAlias
        DiscordId is the key for the selection.
        If DiscordId is not yet in UserMap table it will be added 
        with the provided alias.
        """
        conn = self.conn
        UserMap = {}
        cur = conn.cursor()

        query = "select * from UserMap where DiscordId=?"
        logger.info(query)
        logger.info(f"DiscordId: {DiscordId}")
        logger.info(f"type(DiscordId): {type(DiscordId)}")
        if Alias == None:
            Alias = DiscordId
        try:
            cur.execute(query, [DiscordId])
        except Exception as e:
            logger.info(f"Exception: {e}")
        rowcount = len(cur.fetchall())
        logger.info(f"rowcount {rowcount}")
        if rowcount == 0:
            logger.info(f"User {DiscordId} doesn't exist in UserMap (yet)")
            query = f"insert into UserMap values (?, ?, ?)"
            logger.info(query)
            cur.execute(query, [DiscordId, Alias, Alias])
            UserMap = {'DiscordId': DiscordId, 'DiscordAlias': Alias, 'GsheetAlias': Alias} 
        else:
            query = f"select DiscordId, DiscordAlias, GsheetAlias from UserMap where DiscordId=?"
            cur.execute(query, [DiscordId])
            row = cur.fetchone()
            UserMap = {'DiscordId': row[0], 'DiscordAlias': row[1], 'GsheetAlias': row[2]} 
        logger.info(f"UserMap: DiscordId{UserMap['DiscordId']}, DiscordAlias->{UserMap['DiscordAlias']}, GsheetAlias->{UserMap['GsheetAlias']}")

        return UserMap