"""
This file contains the main functions and classes for Robin.
"""
from discord.ext import commands
from loguru import logger


class Robin(commands.Cog):
    """
    The master class for Robin.
    """

    def __init__(self, bot=None, db=None):
        self.bot = bot
        self.db = db
        logger.info(f"Class {type(self).__name__} initialized from Robin class")

    def _getusermap(self, memberid):
        """
        Get the mapping for discordalias and gsheetalias
        Id is the key for the selection.
        with the provided alias.
        """
        usermap = {}
        usermap = (
            self.db.session.query(
                self.db.User.UserId,
                self.db.User.DiscordId,
                self.db.User.DiscordAlias,
                self.db.User.GsheetAlias,
            ).filter(self.db.User.UserId == memberid)
        ).one()

        return usermap

    def _getusermap_by_alias(self, alias):
        """
        Get the mapping for discordalias and gsheetalias
        Id is the key for the selection.
        with the provided alias.
        """
        usermap = {}
        usermap = (
            self.db.session.query(
                self.db.User.UserId,
                self.db.User.DiscordId,
                self.db.User.DiscordAlias,
                self.db.User.GsheetAlias,
            ).filter(self.db.User.DiscordAlias == alias)
        ).one()

        return usermap

    def _known_user(self, user):
        """
        is there info about the user
        """
        return (
            self.db.session.query(self.db.User)
            .filter(self.db.User.DiscordAlias == user)
            .count()
        )
