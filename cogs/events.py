import discord
from discord.ext import commands
import aiosqlite
from db import dbupdate, getWelcomeChannel
from discord.utils import get

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #When bot joins a server it adds it to the DB
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await dbupdate('main.db', 'INSERT INTO servers (server, name) VALUES (?, ?)', (guild.id, guild.name))
        print(f'{guild.name} added to DB')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcomeChannel = await getWelcomeChannel(member.guild)
        if welcomeChannel is None:
            await member.guild.system_channel.send(f'Welcome {member.mention} to {member.guild.name}')
        else:
            await member.guild.system_channel.send(f'Welcome {member.mention} to {member.guild.name}!\nHead over to {welcomeChannel.mention} to get started!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await member.guild.system_channel.send(f'`{member}` has left {member.guild.name}')
    
    @commands.Cog.listener()
    async def on_guild_update(self, guildOLD, guildNEW):
        if guildNEW.name != guildOLD.name:
            await dbupdate('main.db', 'UPDATE servers SET name=? WHERE server=?', (guildNEW.name, guildNEW.id))
def setup(bot):
    bot.add_cog(Events(bot))