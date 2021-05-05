
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
        help=("Geeft een overzicht van alle rollen in de guild terug."),
        brief="Hiermee update je je status in het status kanaal",
        hidden="True"
    )
    async def get_roles(self, ctx, *args):
        # g: discord.Guild = ctx.guild
        g = ctx.guild

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
