import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(color=0xEE7700)
        embed.set_author(name='FyreBot', icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Language", value="[Python](https://discord.gg/python) | [Discord.py](https://discord.gg/dpy)", inline=False)
        embed.add_field(name="Creator", value="spragouu#8197\n[Twitter](https://twitter.com/spragouu) | [Portfolio](https://portfolio.deadfyre.com/) | [Instagram](https://instagram.com/spragouu)", inline=False)
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))