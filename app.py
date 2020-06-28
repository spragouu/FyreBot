import discord
from discord.ext import commands
import config

bot = commands.Bot(command_prefix='!', case_insensitive=True)

@bot.event
async def on_ready():
    print('Successfully logged in as {0.user}'.format(bot))

@bot.command()
async def load(ctx, extension):
    """Load a cog"""
    bot.load_extension(f'cogs.{extension}')
    await ctx.message.add_reaction('\U00002705')
    

@bot.command()
async def unload(ctx, extension):
    """Unload a cog"""
    bot.unload_extension(f'cogs.{extension}')
    await ctx.message.add_reaction('\U00002705')

@bot.command()
async def reload(ctx, extension):
    """Reload a cog"""
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.message.add_reaction('\U00002705')

bot.run(config.token)