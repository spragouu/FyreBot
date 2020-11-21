import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def send(self, ctx, channel: discord.TextChannel , *message):
        '''Send a message to a specific channel'''
        await channel.send(' '.join(message))

def setup(bot):
    bot.add_cog(Misc(bot))