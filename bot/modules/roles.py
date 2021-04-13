
import discord
import os
# import signal
from datetime import datetime
from discord.ext import commands
from loguru import logger
from .robin import Robin

class Roles(Robin):

    @commands.command(
        name="get_roles",
        help=("Met het status commando update je status in het status kanaal,"
        " hiermee help je je mede ws-ers op de hoogte te houden hoe snel je kunt reageren."),        
        brief="Hiermee update je je status in het status kanaal",
        )
    async def get_roles(self, ctx, *args):
        g: discord.Guild = ctx.guild

        all_roles = await g.fetch_roles() #(ctx.author.id)
        msg = ''
        for role in all_roles:
            msg += f"role.name: {role.name}\n"
        await ctx.send(f"{msg}")
