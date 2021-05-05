import discord
from discord.ext import commands
from loguru import logger
from discord.utils import get


class Robin(commands.Cog):
    def __init__(self, bot=None, conn=None):
        self.bot = bot
        self.conn = conn
        logger.info(f"Class {type(self).__name__} initialized from Robin class")

    def _sanitize(self,
                  msg_in: str,
                  maxlength: int = 200
                  ) -> str:
        """
        Sanitize the message in, remove forbidden characters.
        Truncate the message at maxlength (last bit will be replace with truncated)

        parameters:
          msg_in:    string to be sanitized
          maxlenght: maximum length of the string
        """
        forbidden = ['@', '#']
        trunctext = ' .. truncated'
        logger.info(f"msg_in: {msg_in}")
        if len(msg_in) > maxlength:
            tmplength = maxlength - len(trunctext)
            logger.info(f"tmplength {tmplength}")
            if tmplength < 0:
                msg_out = trunctext
            else:
                msg_out = msg_in[:tmplength]
                msg_out += trunctext
        else:
            msg_out = msg_in

        for nogo in forbidden:
            msg_out = msg_out.replace(nogo, '_')
        return(msg_out)

    async def _feedback(self,
                        ctx: commands.Context = None,
                        msg: str = '',
                        delete_after: int = None,
                        delete_message: bool = False
                        ) -> str:
        """
        Send feedback to the user after a message is posted.
        The original message can be deleted.
        The feedback will be sent to the original channel.

        paramters:
          msg:            the message to send
          delete_after:   how long to wait to delete the feedback message (default keep)
          delete_message: delete the original message (default keep)
        """
        if delete_message is not True and delete_message is not False:
            return f"Invallid option for delete_message {delete_message}"

        if ctx is None:
            return "context not spedified"

        await ctx.send(content=msg, delete_after=delete_after)
        if delete_message:
            try:
                await ctx.message.delete()
            except Exception as e:
                logger.info(f"message deletion failed {e}")
                return f"message deletion failed {e}"
        return "feedback sent successful"

    def _getusermap(self, id):
        """
        Get the mapping for discordalias and gsheetalias
        Id is the key for the selection.
        with the provided alias.
        """
        conn = self.conn
        usermap = {}
        cur = conn.cursor()

        query = f"select Id, DiscordId, discordalias, gsheetalias from usermap where Id=?"
        cur.execute(query, [id])
        row = cur.fetchone()
        usermap = {'Id': row[0], 'discordid': row[1], 'discordalias': row[2], 'gsheetalias': row[3]}
        return(usermap)
