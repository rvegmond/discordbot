import discord
from discord.ext import commands
from loguru import logger
from discord.utils import get


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
        logger.info(f"usermap: discordid->{usermap['discordid']}, discordalias->{usermap['discordalias']}, gsheetalias->{usermap['gsheetalias']}")

        return(usermap)

    # @commands.command()
    def _rolemembers(self, ctx, *args):  # Always same role, no input needed
        guild = ctx.guild
        role_name = args[0]
        role_id = get(guild.roles, name=role_name)

        members = []
        x = role_id.members
        for t in x:
            members.append(t.id)
        return members
