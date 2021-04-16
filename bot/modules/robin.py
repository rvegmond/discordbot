import discord
from discord.ext import commands
from loguru import logger


class Robin(commands.Cog):
    def __init__(self, bot, conn=None):
        self.bot = bot
        self.conn = conn
        logger.info(f"Class {type(self).__name__} initialized ")


    def _sanitize(self, msg_in: str, maxlength=200) -> str:
        """
        Sanitize the message in, remove forbidden characters.
        Truncate the message at maxlength (last bit will be replace with truncated)

        parameters:
          msg_in:    string to be sanitized
          maxlenght: maximum length of the string
        """
        forbidden = ['@', '#']
        logger.info(f"msg_in: {msg_in}")
        if len(msg_in) > maxlength:
            tmplength = maxlength - len(' .. truncated')
            logger.info(f"tmplength {tmplength}")
            if tmplength < 0:
                msg_out = ' .. truncated'
            else:
                msg_out = msg_in[:tmplength]
                msg_out += ' .. truncated'
        else:
            msg_out = msg_in

        for nogo in forbidden:
            msg_out = msg_out.replace(nogo, '_')
        return(msg_out)

    async def _feedback(self, ctx, msg: str, delete_after=None, delete_message=False) -> str:
        """
        Send feedback to the user after a message is posted. 
        The original message can be deleted.
        The feedback will be sent to the original channel.

        paramters:
          msg:            the message to send
          delete_after:   how long to wait to delete the feedback message (default keep)
          delete_message: delete the original message (default keep)
        """ 
        await ctx.send(content=msg, delete_after=delete_after)
        if delete_message:
            try:
                await ctx.message.delete()
            except Exception as e: 
                logger.info(f"message deletion failed {e}")
                return f"message deletion failed {e}"
        return "feedback sent successful"

    def _getusermap(self, discordid, alias=None):
        """
        Get the mapping for discordalias and gsheetalias
        DiscordId is the key for the selection.
        If DiscordId is not yet in usermap table it will be added 
        with the provided alias.
        """
        conn = self.conn
        usermap = {}
        cur = conn.cursor()

        query = "select * from usermap where DiscordId=?"
        logger.info(query)
        logger.info(f"discordid: {discordid}")
        logger.info(f"type(discordid): {type(discordid)}")
        if alias == None:
            alias = discordid
        try:
            cur.execute(query, [discordid])
        except Exception as e:
            logger.info(f"Exception: {e}")
        rowcount = len(cur.fetchall())
        logger.info(f"rowcount {rowcount}")
        if rowcount == 0:
            logger.info(f"User {discordid} doesn't exist in usermap (yet)")
            query = f"insert into usermap values (?, ?, ?)"
            logger.info(query)
            cur.execute(query, [discordid, alias, alias])
            usermap = {'discordid': discordid, 'discordalias': alias, 'gsheetalias': alias} 
        else:
            query = f"select DiscordId, discordalias, gsheetalias from usermap where DiscordId=?"
            cur.execute(query, [discordid])
            row = cur.fetchone()
            usermap = {'discordid': row[0], 'discordalias': row[1], 'gsheetalias': row[2]} 
        logger.info(f"usermap: discordid->{usermap['discordid']}, discordalias->{usermap['discordalias']}, gsheetalias->{usermap['gsheetalias']}")

        return(usermap)