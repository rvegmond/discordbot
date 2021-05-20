"""
This file contains the Roles Class, all functions related to roles should be in here.
"""
from discord.ext import commands
from loguru import logger
from .robin import Robin, _feedback


class Roles(Robin):
    """
    The class that contains the Role related functions
    """
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
        guild = ctx.guild
        all_roles = guild.roles
        msg = ''
        for role in all_roles:
            msg += f"role.name: {role.name}\n"
        await _feedback(ctx, msg=msg)

    async def in_role(self,
                      ctx: commands.Context,
                      req_role: str
                      ) -> bool:
        """
        Check if the author of the message is a member of the specified role.

        paramters:
          req_role:        The role where to check membership on.
        """
        for role in ctx.author.roles:
            if role.name == req_role:
                return True
        return False


def _rolemembers(ctx: commands.Context,
                 role_name: str
                 ) -> list:
    """
    Get a list of members of a specified role.

    paramters:
        role_name:        The role where to get the members of.
    """
    members = []
    guild = ctx.guild
    for role in guild.roles:
        if role.name == role_name:
            logger.info(f"found members for {role_name}")
            role_members = role.members
            break
    for role_member in role_members:
        members.append(role_member.id)
    return members
