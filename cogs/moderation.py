import discord
from db import dbupdate, dbselect
from discord.ext import commands
from discord.utils import get, find
from cogs.log import *


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def permissions(**perms):
        original = commands.has_permissions(**perms).predicate
        async def extended_check(ctx):
            if ctx.guild is None:
                return False
            return ctx.guild.owner_id == ctx.author.id or await original(ctx)
        return commands.check(extended_check)

    #ban user
    @commands.command()
    @permissions(ban_members = True)
    async def ban(self, ctx, bannedUser: discord.User, *reasonForBan):
        '''Ban a user'''
        for e in await ctx.guild.bans():
            if e.user == bannedUser:
                raise Exception(f'{bannedUser} is already banned')

        formattedReason = ' '.join(reasonForBan)
        if not formattedReason:
            formattedReason = 'None Provided'

        await ctx.guild.ban(bannedUser, reason = formattedReason)
        await ctx.send(f'{bannedUser.mention} has been banned')
        await member_ban(ctx.guild, bannedUser, ctx.message.author, formattedReason)
        
    #unban user
    @commands.command()
    @permissions(ban_members = True)
    async def unban(self, ctx, unbannedUser: discord.User, *reasonForUnban):
        '''Unban a user'''
        for e in await ctx.guild.bans():
            if e.user == unbannedUser:
                formattedReason = ' '.join(reasonForUnban)
                if not formattedReason:
                    formattedReason = 'None Provided'

                await ctx.guild.unban(unbannedUser, reason = formattedReason)
                await ctx.send(f'{unbannedUser.mention} has been unbanned')
                await member_unban(ctx.guild, unbannedUser, ctx.message.author, formattedReason)
                return   
        
        raise Exception(f'{unbannedUser} is not banned')

    #kick user
    @commands.command()
    @permissions(kick_members = True)
    async def kick(self, ctx, kickedUser: discord.User, *reasonForKick):
        '''Kick a user'''
        if kickedUser in ctx.guild.members:
            formattedReason = ' '.join(reasonForKick)
            if not formattedReason:
                formattedReason = 'None Provided'

            await ctx.guild.kick(kickedUser)
            await ctx.send(f'{kickedUser.mention} has been kicked')
            await member_kicked(ctx.guild, kickedUser, ctx.message.author, formattedReason)
        else:
            raise Exception(f'{kickedUser} is not in the server')

    #mute setup
    @commands.command()
    @permissions(administrator = True)
    async def muteSetup(self, ctx):
        '''Setup the mute role and permissions'''
        #Check to make sure the mute role isn't already setup
        muteRoleID = await dbselect('main.db', 'SELECT mute_role FROM servers WHERE server=?', (ctx.guild.id,))

        if muteRoleID is not None:
            #check if the guild has a role linked to the muteRoleID
            muteRole = get(ctx.guild.roles, id = muteRoleID)
            if muteRole is not None:
                raise Exception('A "Muted" role has already been setup. Exiting setup')

        muteRole = await ctx.guild.create_role(name='Muted')

        permsOverwrite = discord.PermissionOverwrite()
        permsOverwrite.send_messages = False

        #update server category permissions
        categories = ctx.guild.categories
        for c in categories:
            await c.set_permissions(muteRole, overwrite = permsOverwrite)
        #update server text channels permissions
        channels = ctx.guild.text_channels
        for c in channels:
            await c.set_permissions(muteRole, overwrite = permsOverwrite)

        await dbupdate('main.db', 'UPDATE servers SET mute_role=? WHERE server=?', (muteRole.id, ctx.guild.id))
        await ctx.send('```✅ Success:\n    ↪️ Muted role created\n    ↪️ Category and channel permissions updated```')

    #mute user
    @commands.command()
    @permissions(mute_members = True)
    async def mute(self, ctx, member: discord.Member, *reasonForMute):
        '''Mute a user'''
        #get mute role from DB
        muteRoleID = await dbselect('main.db', 'SELECT mute_role FROM servers WHERE server=?', (ctx.guild.id,))
        #check if !mutesetup was run
        if muteRoleID is None:
            raise Exception('You need to run the mute setup to use the mute commands')

        muteRole = get(ctx.guild.roles, id = muteRoleID)
        #check if the Muted role was deleted from the guild
        if muteRole is None:
            raise Exception(f"{ctx.guild.name}'s 'Muted' role has been deleted. Please run the setup command to use the mute commands again")

        #verify user isn't themself or already muted - if not add the role
        if member.id == ctx.message.author.id:
            raise Exception('You cannot mute yourself')
        elif muteRole in member.roles:
            raise Exception(f'{member.name} is already muted')
        else:
            await member.add_roles(muteRole)
            formattedReason = ' '.join(reasonForMute)
            if not formattedReason:
                formattedReason = 'None Provided'
            await member_mute(ctx.guild, muteRole, member, ctx.message.author, formattedReason)


    #unmute user
    @commands.command()
    @permissions(mute_members = True)
    async def unmute(self, ctx, member: discord.Member, *reasonForUnmute):
        '''Unmute a user'''
        #get mute role from DB
        muteRoleID = await dbselect('main.db', 'SELECT mute_role FROM servers WHERE server=?', (ctx.guild.id,))
        #check if !mutesetup was run
        if muteRoleID is None:
            raise Exception('You need to run the mute setup to use the mute commands')

        muteRole = get(ctx.guild.roles, id = muteRoleID)
        #check if the Muted role was deleted from the guild
        if muteRole is None:
            raise Exception(f"{ctx.guild.name}'s 'Muted' role has been deleted. Please run the setup command to use the mute commands again")

        #check if user actually has mute role
        if muteRole in member.roles:
            #remove role from user
            await member.remove_roles(muteRole)
            formattedReason = ' '.join(reasonForUnmute)
            if not formattedReason:
                formattedReason = 'None Provided'
            await member_unmute(ctx.guild, muteRole, member, ctx.message.author, formattedReason)
        else:
            raise Exception(f"{member.name} isn't muted")

    #purge
    @commands.command()
    @permissions(manage_messages = True)
    async def purge(self, ctx, amount: int):
        '''Delete a specified number of messages'''
        await ctx.channel.purge(limit = amount+1)


def setup(bot):
    bot.add_cog(Moderation(bot))