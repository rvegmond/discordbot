
import discord
import os
# import signal
from datetime import datetime
from discord.ext import commands
from loguru import logger
from .robin import Robin
from discord.utils import get

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

    # @commands.command()
    async def rolemembers(self, ctx, *args): # Always same role, no input needed
        guild = ctx.guild
        role_name = args[0] 
        role_id = get(guild.roles, name=role_name)

        members = []
        await ctx.send(f"role: {role_name}, id: {role_id} ")
        x = role_id.members
        await ctx.send(f"len: {len(x)}")
        for t in x.toL:
            await ctx.send(f"member: {t}")
            members.append(t.name)
        await ctx.send(f"members: {members}")
        await ctx.send(f"type(members): {type(members)}")

        return members