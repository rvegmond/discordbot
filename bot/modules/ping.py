import discord
from discord.ext import commands
from threading import Lock
from .robin import Robin


class Ping(Robin):
    # @commands.command(name='ping', hidden=False)
    # @commands.max_concurrency(1, wait=True)
    # @commands.guild_only()
    @commands.command(
        
        name="ping",
        help=("Commando om te zien of de bot nog leeft."
        "Als de bot een redelijk blije bot is krijg je en pong terug."
        "Een blije bot is geen garantie op succes en gezondheid...."),        
        brief="Commando om te zien of de bot nog leeft.",
        )
    async def ping(self, ctx):
        await ctx.send(f"pong")
