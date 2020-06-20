import discord
import config

client = discord.Client()

prefix = '!'

@client.event
async def on_ready():
    print('Successfully logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(prefix + 'ping'):
        await message.channel.send('pong')

client.run(config.token)