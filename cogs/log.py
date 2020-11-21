import discord
from discord.ext import commands
from discord.utils import get
from db import dbupdate, dbselect, getLogChannel




class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def permissionsCheck(self, ctx):
        original = commands.has_permissions(administrator=True).predicate
        if ctx.guild.owner_id == ctx.author.id or ctx.author.id in ctx.bot.owner_ids or await original(ctx):
            return True
        await ctx.send("You do not have permissions to do that.", delete_after=10)
        return False

    @commands.command()
    async def setup(self, ctx, logChannel: discord.TextChannel):
        '''Setup logging in the server'''
        #Get log_channel value from DB
        dbLogChannelID = await dbselect('main.db', 'SELECT log_channel FROM servers WHERE server=?', (ctx.guild.id,))
        #Check to see if the DB returned a value or None
        if dbLogChannelID is not None:
            #Check if the db channel is in the server
            if get(ctx.guild.channels, id = dbLogChannelID) is not None:
                    raise Exception(f'{ctx.guild.name} already has a log channel setup')

        #Set log channel in DB
        await dbupdate('main.db', 'UPDATE servers SET log_channel=? WHERE server=?', (logChannel.id, ctx.guild.id))
        #Send confirmation message
        await ctx.send('```✅ Success:\n    ↪️ Log channel assigned```')

    #message edited
    @commands.Cog.listener()
    async def on_message_edit(self, messageOLD, messageNEW):
        logChannel = await getLogChannel(messageNEW.guild)
        if logChannel is None:
            return
        elif messageOLD.content == '' or messageNEW.content == '':
            return
        elif messageOLD.author.bot:
            return
            
        embed = discord.Embed(title = "Message Edited", 
            description = f'Edited by: {messageNEW.author.mention}', 
            color=0xe8a415)
        embed.add_field(name = "Before", value = messageOLD.content, inline = True)
        embed.add_field(name = "After", value = messageNEW.content, inline = True)
        await logChannel.send(embed = embed)

    #message deleted
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        logChannel = await getLogChannel(message.guild)
        if logChannel is None:
            return

        if len(message.attachments) > 0 :
            messageURLs = []
            for a in message.attachments:
                messageURLs.append(a.url)
            embed = discord.Embed(title = f'Message Deleted', description = f'Author: {message.author.mention}\nMessage Content: \n{message.content}\nMessage Attachments: \n{messageURLs}', color = 0xe8a415)
        else:
            embed = discord.Embed(title = f'Message Deleted', description = f'Author: {message.author.mention}\nMessage Content: \n{message.content}', color = 0xe8a415)
        await logChannel.send(embed = embed)

    #messages bulk deleted(purge)
    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        memberWhoPurged = messages[len(messages) - 1].author
        messages.pop(len(messages) - 1) #remove the last deleted message (the purge command)
        logChannel = await getLogChannel(messages[1].guild)
        if logChannel is None:
            return

        embed = discord.Embed(
            title = "Messages Deleted (Purge)", 
            description = f'Mass delete by: {memberWhoPurged.mention}\nMessages deleted: {len(messages)}',
            color = 0xe8a415)
        for m in messages:
            if len(m.attachments) > 0 :
                newlist = []
                for a in m.attachments:
                    newlist.append(a.url)
                embed.add_field(name = f'Message {messages.index(m) + 1}', value = f'Author: {m.author.mention}\nMessage Content: \n{m.content}\nMessage Attachments: \n{newlist}', inline = False)
            else:
                embed.add_field(name = f'Message {messages.index(m) + 1}', value = f'Author: {m.author.mention}\nMessage Content: \n{m.content}', inline = False)
        await logChannel.send(embed = embed)

#user banned - Indented in as it's a custom event and can't be within the log class
@commands.Cog.listener()
async def member_ban(guild, bannedUser, bannedBy, reason):
    logChannel = await getLogChannel(guild)
    if logChannel is None:
        return

    embed = discord.Embed(
        title = "Member Banned", 
        description = f'Banned member: {bannedUser.mention}\nBanned by: {bannedBy.mention}\nReason: {reason}',
        color = 0xe8a415)
    await logChannel.send(embed = embed)

#user unbanned - Indented in as it's a custom event and can't be within the log class
@commands.Cog.listener()
async def member_unban(guild, unbannedUser, unbannedBy, reason):
    logChannel = await getLogChannel(guild)
    if logChannel is None:
        return

    embed = discord.Embed(
        title = "Member Unbanned", 
        description = f'Unbanned member: {unbannedUser.mention}\nUnbanned by: {unbannedBy.mention}\nReason: {reason}',
        color = 0xe8a415)
    await logChannel.send(embed = embed)

#user kicked - Indented in as it's a custom event and can't be within the log class
async def member_kicked(guild, kickedMember, kickedBy, reason):
    logChannel = await getLogChannel(guild)
    if logChannel is None:
        return

    embed = discord.Embed(
        title = "Member Kicked", 
        description = f'Kicked member: {kickedMember.mention}\nKicked by: {kickedBy.mention}\nReason: {reason}',
        color = 0xe8a415)
    await logChannel.send(embed = embed)

#user muted
async def member_mute(guild, muteRole, mutedUser, mutedBy, reason):
    logChannel = await getLogChannel(guild)
    if logChannel is None:
        return

    embed = discord.Embed(
        title = "Member Muted", 
        description = f'Muted member: {mutedUser.mention}\nMuted by: {mutedBy.mention}\nReason: {reason}',
        color = 0xe8a415)
    await logChannel.send(embed = embed)

#user unmuted
async def member_unmute(guild, muteRole, unmutedUser, unmutedBy, reason):
    logChannel = await getLogChannel(guild)
    if logChannel is None:
        return

    embed = discord.Embed(
        title = "Member Unmuted", 
        description = f'Unmuted member: {unmutedUser.mention}\nUnmuted by: {unmutedBy.mention}\nReason: {reason}',
        color = 0xe8a415)
    await logChannel.send(embed = embed)
        
def setup(bot):
    bot.add_cog(Log(bot))