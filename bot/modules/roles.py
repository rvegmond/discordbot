
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

        all_roles = await g.fetch_roles() #(ctx.message.author.roles)
        msg = ''
        for role in all_roles:
            msg += f"role.name: {role.name}\n"
        await ctx.send(f"{msg}")

    @commands.command(
        name="wawa"
    )
    async def wawa(self, ctx, *args):
        server = ctx.message.server
        default_name = DEFAULT_ROLE_NAME
        role_id = self.json.get(server.id, {}).get('ROLE_ID')

        if role_id:
            role = discord.utils.get(server.roles, id=role_id)
        else:
            role = discord.utils.get(server.roles, name=default_name)

        perms = server.me.server_permissions
        if not (perms.manage_roles and perms.manage_channels):
            await self.bot.say("I need the Manage Roles and Manage Channels permissions for that command to work.")
            return
            
async def in_role(self, ctx, *args):
    req_role = args[0]
    await ctx.send(f"req_role {req_role}")
    await ctx.send(f"ctx.author.roles {ctx.author.roles}")
    for role in ctx.author.roles:
        if role.name == req_role:
            await ctx.send(f"role.name {role.name}")
            return True
    return False

        
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
