import discord
from discord.ext import commands
from pathlib import Path
from db import dbupdate, dbselect
from discord.utils import get

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        original = commands.has_permissions(administrator=True).predicate
        if ctx.guild.owner_id == ctx.author.id or ctx.author.id in ctx.bot.owner_ids or await original(ctx):
            return True
        await ctx.send("You do not have permissions to do that.", delete_after=10)
        return False

    @commands.command()
    async def setWelcome(self, ctx, welcomeChannel: discord.TextChannel):
        '''Set the welcome channel '''
        #Get welcome_channel value from DB
        dbWelcomeChannelID = await dbselect('main.db', 'SELECT welcome_channel FROM servers WHERE server=?', (ctx.guild.id,))
        #Check to see if the DB returned a value or None
        if dbWelcomeChannelID is not None:
            #Check if the db channel is in the server
            if get(ctx.guild.channels, id = dbWelcomeChannelID) is not None:
                    raise Exception(f'{ctx.guild.name} already has a welcome channel setup')

        #Set welcome channel in DB
        await dbupdate('main.db', 'UPDATE servers SET welcome_channel=? WHERE server=?', (welcomeChannel.id, ctx.guild.id))
        #Send confirmation message
        await ctx.send('```✅ Success:\n    ↪️ Welcome channel assigned```')

    @commands.command(usage = '<YourRolesChannel> <YourWelcomeChannel>')
    async def welcome(self, ctx, roleChannel: discord.TextChannel, channel: discord.TextChannel):
        '''Send the server's welcome/info message to a specific channel'''
        imgPath = Path("./images/")
        if channel is None:
            channel = ctx
        
        await channel.send(file = discord.File(imgPath / 'Welcome Neon.png'))
        await channel.send(file = discord.File(imgPath / 'Divider Neon.png'))

        await channel.send("This is a community created by spragouu for friends to hang out, all with the common interests of video games and tech.\n\nInitially DeadFyre was a project spragouu started that had no end goal and to this day still remains a mystery of its true purpose. Since it has evolved it has been used as a team name used in various competitions, predominantly in Rocket League, and it's main purpose now is this discord community.\n\nIf you're here you're probably a friend of spragouu or you have a mutual friend. Whatever the case, welcome, enjoy your stay, and have fun.")

        await channel.send(file = discord.File(imgPath / 'Divider Neon.png'))

        await channel.send(f"The first step to begin interacting within the server is to get yourself some roles.\nHead over to {roleChannel.mention} to setup your server roles!")

        await channel.send(file = discord.File(imgPath / 'Divider Neon.png'))

        await channel.send("Discord: https://discord.gg/uaxgEhu")

        await channel.send(file = discord.File(imgPath / 'Divider Neon.png'))

def setup(bot):
    bot.add_cog(Welcome(bot))