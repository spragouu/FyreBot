import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def send(self, ctx, channel: discord.TextChannel , *message):
        '''Send a message to a specific channel'''
        await channel.send(' '.join(message))

    @commands.command()
    async def edit(self, ctx, messageID, newMessage, channel: discord.TextChannel = None):
        '''Edit a message send by the bot'''
        if (channel is None):
            try:
                message = await ctx.fetch_message(messageID)
                await message.edit(content = newMessage)
            except:
                raise Exception("That message doesn't exist in this channel. Please specify the channel the message is in!")
        else:
            try:
                message = await channel.fetch_message(messageID)
                await message.edit(content = newMessage)
            except:
                raise Exception("That message doesn't exist in the specified channel!")

def setup(bot):
    bot.add_cog(Misc(bot))