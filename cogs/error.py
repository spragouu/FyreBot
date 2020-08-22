import discord
import sys
import traceback
from discord.ext import commands

class Error(commands.Cog):
    def __init__k(self, bot):
        self.bot = bot

    #Basic Error handling
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #React to a command that had an error with ❌
        await ctx.message.add_reaction('❌')

        #Post traceback to console
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

        #Post error in ctx channel
        error = getattr(error, 'original', error)
        await ctx.send(f"```❌ Error Detected:\n    ↪️ {error}```")

def setup(bot):
    bot.add_cog(Error(bot))