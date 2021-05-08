
import discord
import os
from datetime import datetime
from discord.ext import commands
from loguru import logger
from .robin import Robin
from discord.utils import get


class Roles(Robin):

    @commands.command(
        name="get_all_roles",
        help="Geeft een overzicht van alle rollen in de guild terug.",
        brief="Geeft een overzicht van alle rollen in de guild terug.",
        hidden="True"
    )
    def all_roles(self,
                  ctx: commands.Context
                  ) -> str:
        """
        Get a list of all roles in the guild, lined up.
        """
        g = ctx.guild
        all_roles = g.roles
        msg = ''
        for role in all_roles:
            msg += f"role.name: {role.name}\n"
        logger.info("msg: {msg}")

    def _get_all_roles(self,
                       ctx: commands.Context
                       ) -> str:
        """
        Get a list of all roles in the guild, lined up.
        """
        g = ctx.guild
        all_roles = g.roles
        msg = ''
        for role in all_roles:
            msg += f"role.name: {role.name}\n"
        return msg

    @commands.command(
        name="get_all_roles",
        help="Geeft een overzicht van alle rollen in de guild terug.",
        brief="Geeft een overzicht van alle rollen in de guild terug.",
        hidden="True"
    )
    async def get_all_roles(self,
                            ctx: commands.Context
                            ):
        """
        Get a list of all roles in the guild, lined up. (wrapper function)
        """
        msg = self._get_roles(ctx)
        await self._feedback(ctx, msg)

    async def in_role(self,
                      ctx: commands.Context,
                      req_role: str
                      ) -> bool:
        for role in ctx.author.roles:
            if role.name == req_role:
                return True
        return False

    # @commands.command()
    def _rolemembers(self,
                     ctx: commands.Context,
                     role_name: str
                     ) -> list:
        """
        Get a list of members of a specified role.

        paramters:
          role_name:        The role where to get the members of.
        """
        guild = ctx.guild
        role_id = get(guild.roles, name=role_name)

        members = []
        x = role_id.members
        for t in x:
            members.append(t.id)
        return members
