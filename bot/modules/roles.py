
import discord
import os
from datetime import datetime
from discord.ext import commands
from loguru import logger
from .robin import Robin
from discord.utils import get


class Roles(Robin):

    def _get_roles(self, ctx):
        g = ctx.guild
        all_roles = g.roles
        msg = ''
        for role in all_roles:
            msg += f"role.name: {role.name}\n"
        return msg

    @commands.command(
        name="get_roles",
        help="Geeft een overzicht van alle rollen in de guild terug.",
        brief="Geeft een overzicht van alle rollen in de guild terug.",
        hidden="True"
    )
    async def get_roles(self, ctx):
        msg = self._get_roles(ctx)
        await self._feedback(ctx, msg)

    async def in_role(self, ctx, req_role: str):
        for role in ctx.author.roles:
            if role.name == req_role:
                return True
        return False

    # @commands.command()
    def _rolemembers(self, ctx, role_name: str):
        guild = ctx.guild
        role_id = get(guild.roles, name=role_name)

        members = []
        x = role_id.members
        for t in x:
            members.append(t.id)
        return members
