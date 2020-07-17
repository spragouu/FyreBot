import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(title=f'Welcome to {member.guild.name}!', color=0xbe5f00, description='Thanks for joining us!')
        embed.set_footer(icon_url=self.bot.user.avatar_url)
        embed.set_author(name=f'{member.name}#{member.discriminator}', icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.guild.icon_url)

        await member.send(embed=embed)

def setup(bot):
    bot.add_cog(Events(bot))