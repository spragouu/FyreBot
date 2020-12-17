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
        
        await channel.send(file = discord.File(imgPath / 'Welcome.png'))
        await channel.send(file = discord.File(imgPath / 'Divider.png'))

        await channel.send('Welcome to the DeadFyre discord server!\nTo get started head over to #dev to select your proper roles.\n\n__**Server Rules**__\n\n- The one rule is Use Common Sense. Things like spamming, Not using proper channels, arguing or causing drama, excessive swearing, racism, and so on.\nThis rule will be enforced at our discretion.')

        await channel.send(file = discord.File(imgPath / 'Divider.png'))

        await channel.send('__**Links**__\n\nWebsite: https://deadfyre.com/\nDiscord: https://discord.gg/uaxgEhu')

        await channel.send(file = discord.File(imgPath / 'Divider.png'))

def setup(bot):
    bot.add_cog(Welcome(bot))