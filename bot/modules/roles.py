
import discord
import os
# import signal
from datetime import datetime
from discord.ext import commands
from loguru import logger
from .robin import Robin

class Roles(Robin):

    @commands.command(
        name="get_roles",
        help=("Met het status commando update je status in het status kanaal,"
        " hiermee help je je mede ws-ers op de hoogte te houden hoe snel je kunt reageren."),        
        brief="Hiermee update je je status in het status kanaal",
        )
    async def get_roles(self, ctx, *args):
        g: discord.Guild = ctx.guild

        all_roles = await g.fetch_roles() #(ctx.author.id)
        msg = ''
        for role in all_roles:
            msg += f"role.name: {role.name}\n"
        await ctx.send(f"{msg}")

    @commands.command(
        name="in_roles",
        help=("Met het status commando update je status in het status kanaal,"
        " hiermee help je je mede ws-ers op de hoogte te houden hoe snel je kunt reageren."),        
        brief="Hiermee update je je status in het status kanaal",
        )
    async def in_roles(self, ctx, *args):
        # req_role = args[0]

        # g: discord.Guild = ctx.guild

        
        for role in ctx.author.roles:
            await ctx.send(f"role: {role}")
            if role.name == "Test":
                print("USER_ID: %d - ROLE: %s" % (member.id, role.name))

    @commands.command()
    async def team(self, ctx, *args): # Always same role, no input needed
        guild = ctx.message.guild
        tk = guild.get_role(831972238328332288)
        tkm = tk.members
        await ctx.send(f"tkm: {tkm}")
        for row in tkm:   
            a = row.name  
            await ctx.send(f"a: {a}")
            await ctx.send(f"row.name: {row.name}")
            # print(type(a)) # smehows "<class 'discord.member.Member'>" x amount of times
            await ctx.send(a)
