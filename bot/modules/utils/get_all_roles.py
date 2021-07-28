from discord.ext import commands
from loguru import logger
from ..robin import Robin
from ..utils import feedback


class GetAllRoles(Robin):
    """
    The class that contains the Role related functions
    """

    @commands.command(
        name="get_all_roles",
        help="Geeft een overzicht van alle rollen in de guild terug.",
        brief="Geeft een overzicht van alle rollen in de guild terug.",
        hidden="True",
    )
    async def command(self, ctx: commands.Context):
        """
        Get a list of all roles in the guild, lined up. (wrapper function)
        """
        guild = ctx.guild
        all_roles = guild.roles
        msg = ""
        for role in all_roles:
            msg += f"role.name: {role.name}\n"
        await feedback(ctx, msg=msg)
