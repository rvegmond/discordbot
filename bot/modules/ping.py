"""
The contents of this file is to reflect happyness of robin.
"""
from discord.ext import commands
from .robin import Robin, _feedback


class Ping(Robin):
    """
    Are you happy Robin?
    """
    @commands.command(
        name="ping",
        help=("Commando om te zien of de bot nog leeft."
              "Als de bot een redelijk blije bot is krijg je en pong terug."
              "Een blije bot is geen garantie op succes en gezondheid...."),
        brief="Commando om te zien of de bot nog leeft.",
    )
    async def ping(self, ctx):
        """
        Are you there Robin? should reply a pong.
        """
        await _feedback(ctx, msg="pong")   


    @commands.command(
        name="shamrock",
        help=("Commando om te zien of de bot nog leeft."
              "Als de bot een redelijk blije bot is krijg je en pong terug."
              "Een blije bot is geen garantie op succes en gezondheid...."),
        brief="Commando om te zien of de bot nog leeft.",
    )
    async def shamrock(self, ctx):
        """
        Are you there Robin? should reply a pong.
        """
        await _feedback(ctx, msg="Voelt zich niet zo lekker, had gister dat laatste biertje niet moeten nemen...")

    @commands.command(
        name="tassadar",
        help=("Commando om te zien of de bot nog leeft."
              "Als de bot een redelijk blije bot is krijg je en pong terug."
              "Een blije bot is geen garantie op succes en gezondheid...."),
        brief="Commando om te zien of de bot nog leeft.",
    )
    async def tassadar(self, ctx):
        """
        Are you there Robin? should reply a pong.
        """
        await _feedback(ctx, msg="Ach vaderlief, toe drink niet meer... (https://www.youtube.com/watch?v=rBDwUXi1Sbw)")
