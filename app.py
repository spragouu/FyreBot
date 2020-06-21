import discord
from discord.ext import commands
import config

bot = commands.Bot(command_prefix='!', case_insensitive=True)

@bot.event
async def on_ready():
    print('Successfully logged in as {0.user}'.format(bot))

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(config.token)