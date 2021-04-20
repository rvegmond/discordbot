
import discord
import os
from datetime import datetime
from discord.ext import commands
from loguru import logger
from .robin import Robin
from discord.utils import get


class Roles(Robin):

    @commands.command(
        name="get_roles",
        help=("Met het status commando update je status in het status kanaal,"
              " hiermee help je je mede ws-ers op de hoogte te houden hoe snel je kunt reageren."),
        brief="Hiermee update je je status in het status kanaal",
        hidden="True"
    )
    async def get_roles(self, ctx, *args):
        g: discord.Guild = ctx.guild

        all_roles = await g.fetch_roles()
        msg = ''
        for role in all_roles:
            msg += f"role.name: {role.name}\n"
        await ctx.send(f"{msg}")

    async def in_role(self, ctx, *args):
        req_role = args[0]
        for role in ctx.author.roles:
            if role.name == req_role:
                return True
        return False
