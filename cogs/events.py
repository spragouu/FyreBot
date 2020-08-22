import discord
from discord.ext import commands
import aiosqlite
from db import dbupdate

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    #When bot joins a server it adds it to the DB
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await dbupdate('main.db', 'INSERT INTO servers (server, name) VALUES (?, ?)', (guild.id, guild.name))
        print(f'{guild.name} added to DB')
    

def setup(bot):
    bot.add_cog(Events(bot))