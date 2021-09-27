from discord.ext import commands
from loguru import logger

from ..robin import Robin
from ..utils import feedback


class Info(Robin):
    """
    The class that contains the Whitestar functions
    """

    @commands.command(
        name="info",
        help=("Geeft info over een een speler."),
        brief="Geeft info over een speler.",
    )
    async def command(self, ctx, user):

        logger.info(f"user {user}")
        logger.info(f"exists: {self._known_user(user)}")
        if self._known_user(user):
            row = (
                self.db.session.query(self.db.User)
                .filter(self.db.User.DiscordAlias == user)
                .one()
            )

            if row.LastActive is None:
                last_active = "Al even niet actief.."
                last_channel = "niet bekend"
            else:
                last_active = row.LastActive
                last_channel = row.LastChannel
            msg = (
                f"Info over: **{row.DiscordAlias}**\n\n"
                f"DiscordAlias: {row.DiscordAlias}\n"
                f"DiscordId: {row.UserId}\n"
                f"Laatst actief op discord: {last_active}\n"
                f"Laatst actief in kanaal: {last_channel}"
            )
        else:
            msg = f"User: {user} is onbekend."

        await feedback(ctx=ctx, msg=msg)
