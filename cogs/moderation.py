import discord
import db
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #MAKE SURE TO ADD VERIFICATION SO ONE THOSE WITH PROPER PERMISSIONS CAN USE COMMAND!!!

    #ban user
    @commands.command()
    async def ban(self, ctx, user: discord.User):
        await ctx.guild.ban(user)
        await ctx.send(f'{user} has been banned')
        
    #unban user
    @commands.command()
    async def unban(self, ctx, user: discord.User):
        await ctx.guild.unban(user)
        await ctx.send(f'{user} has been unbanned')

    #kick user
    @commands.command()
    async def kick(self, ctx, user: discord.User):
        await ctx.guild.kick(user)
        await ctx.send(f'{user} has been kicked')

    #mute setup
    #@commands.command()
    #async def muteSetup(self, ctx, role: discord.Role):
        #create role
        #set role permissions
        #add role to DB
        #send message confirming setup is complete

    #mute user
    #@commands.command()
    #async def mute(self, ctx, user: discord.User):
        #get mute role from DB
        #add role to user

    #unmute user
    #@commands.command()
    #async def mute(self, ctx, user: discord.User):
        #get mute role from DB
        #check if user actually has mute role
            #remove role from user

    #purge
    @commands.command()
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit = amount+1)


def setup(bot):
    bot.add_cog(Moderation(bot))