from discord.ext import commands
from loguru import logger


async def in_role(self, ctx: commands.Context, req_role: str) -> bool:
    """
    Check if the author of the message is a member of the specified role.

    paramters:
        req_role:        The role where to check membership on.
    """
    for role in ctx.author.roles:
        if role.name == req_role:
            return True
    return False
