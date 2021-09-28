from discord.ext import commands
from loguru import logger

from ..robin import Robin
from ..utils import feedback


class UserAlias(Robin):
    """
    The class that has some alias options (usermap related mostly)
    """

    @commands.command(
        name="get_gsheetalias",
        help=("Vraag je google sheet alias op."),
        brief="Vraag aan Robin wat volgens hem je huidige google sheet alias is.",
    )
    async def get_gsheetalias(self, ctx):
        """
        Get the current gsheet alias from the database (using the usermap function)
        """
        usermap = self._getusermap(int(ctx.author.id))
        msg = f"Google sheet alias voor {ctx.author.name} is {usermap['GsheetAlias']}"
        await feedback(ctx=ctx, msg=msg)

    @commands.command(
        name="set_gsheetalias",
        help=("Pas je google sheet alias aan."),
        brief="Pas voor Robin je alias aan zodat deze overeen komt met wat er in de google sheet staat.",
    )
    async def set_gsheetalias(self, ctx, alias):
        """
        updating the gsheet alias in the database, Will be done only for the user who sends it
        """
        data = {"GsheetAlias": alias}
        self.db.session.query(self.db.User).filter(
            self.db.User.UserId == int(ctx.author.id)
        ).update(data)
        msg = f"google sheet alias aangepast voor {ctx.author.name} naar {alias}"
        await feedback(ctx=ctx, msg=msg)
