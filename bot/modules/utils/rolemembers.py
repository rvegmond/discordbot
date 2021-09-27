from discord.ext import commands
from loguru import logger


def rolemembers(ctx: commands.Context, role_name: str) -> list:
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
