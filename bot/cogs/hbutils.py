import discord
from discord.ext import commands
import tools
from replit import db
from io import BytesIO
import math
import datetime
import time

red = discord.Colour.red()

class Utilitys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx, member: discord.Member = None):
        if member == None:
            embed = discord.Embed(
                title='User Info',
                description='do `hb: info @user` to get info about them')
            embed.add_field(name='Name:', value=ctx.author.name)
            embed.add_field(
                name='Discriminator:', value=ctx.author.discriminator)
            embed.add_field(name='ID:', value=ctx.author.id)
            embed.add_field(name='Bot?', value=ctx.author.bot)
            embed.add_field(
                name='Booster?', value=tools.is_booster(ctx.author))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='User Info',
                description='do `hb: info` to get info about you')
            embed.add_field(name='Name:', value=member.name)
            embed.add_field(name='Discriminator:', value=member.discriminator)
            embed.add_field(name='ID:', value=member.id)
            embed.add_field(name='Bot?', value=member.bot)
            embed.add_field(
                name='Booster?', value=tools.is_booster(member))
            await ctx.send(embed=embed)
    
    @commands.command()
    async def userinfo(self, ctx, user : discord.User):
        embed = discord.Embed(
            title='User Info',
        )
        embed.add_field(name='Name:', value=user.name)
        embed.add_field(name='Discriminator:', value=user.discriminator)
        embed.add_field(name='ID:', value=user.id)
        embed.add_field(name='Bot?', value=user.bot)
        await ctx.send(embed=embed)

    @commands.command(name='botinfo', aliases=['hbinfo'])
    async def botinfo(self, ctx):
        embed = discord.Embed(
            title='henos bot',
            description='use `hb: help` for a list of the commands')
        embed.add_field(name='Name:', value=self.bot.user.name)
        embed.add_field(
            name='Discriminator:', value=self.bot.user.discriminator)
        embed.add_field(name='ID:', value=self.bot.user.id)
        embed.add_field(name='Owner:', value='henos')
        embed.add_field(
            name='Ping:', value=f'{round(self.bot.latency * 1000)} ms')
        embed.add_field(name='Invite:', value='http://tiny.cc/henosbot')
        embed.add_field(name='Servers:', value=len(self.bot.guilds))
        embed.add_field(name='Members:', value=len(self.bot.users))
        embed.add_field(name='Prefixs:', value='hb: , hb:')
        await ctx.send(embed=embed)

    @commands.command(aliases=['serverinfo'])
    async def guildinfo(self, ctx):
        embed = discord.Embed(title='Server Info')
        embed.add_field(name='Name:', value=ctx.guild.name)
        embed.add_field(name='ID:', value=ctx.guild.id)
        embed.add_field(name='Channels:', value=len(ctx.guild.channels))
        embed.add_field(name='Members:', value=len(ctx.guild.members))
        embed.add_field(
            name='Boosts:', value=len(ctx.guild.premium_subscribers))
        embed.add_field(name='Owner:', value=ctx.guild.owner.mention)
        if ctx.guild.id in db['Ignored']:
            ignored = True
        else:
            ignored = False
        embed.add_field(name='Interaction disabled?', value=ignored)
        await ctx.send(embed=embed)

    @commands.command(aliases=['disablelevelup', 'disablewelcome'])
    @commands.has_permissions(manage_guild=True)
    async def disableinteraction(self, ctx):
      ignored = db['Ignored']
      ignored.append(ctx.guild.id)
      db['Ignored'] = ignored
      await ctx.send(f'Guild {ctx.guild.name} has disabled interaction messages.')
    
    @commands.command()
    @commands.is_owner()
    async def text(self, ctx, user : discord.User, *, message):
      msg = await user.send('Incoming text message from my owner...')
      await msg.edit(content=f'Message: {message}')
      await ctx.send('Message sent successfully')
    
    @commands.command()
    @commands.guild_only()
    async def roles(self, ctx):
        """ Get all roles in current server """
        allroles = ""

        for num, role in enumerate(sorted(ctx.guild.roles, reverse=True), start=1):
            allroles += f"[{str(num).zfill(2)}] {role.id}\t{role.name}\t[ Users: {len(role.members)} ]\r\n"

        data = BytesIO(allroles.encode('utf-8'))
        await ctx.send(content=f"Roles in **{ctx.guild.name}**", file=discord.File(data, filename=f"{tools.timetext('Roles')}"))

    @commands.command()
    @commands.guild_only()
    async def joinedat(self, ctx, *, user: discord.Member = None):
        """ Check when a user joined the current server """
        user = user or ctx.author

        embed = discord.Embed()
        embed.set_thumbnail(url=user.avatar_url)
        embed.description = f'**{user}** joined **{ctx.guild.name}**\n{tools.date(user.joined_at)}'
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def mods(self, ctx):
        """ Check which mods are online on current guild """
        message = ""
        all_status = {
            "online": {"users": [], "emoji": "🟢"},
            "idle": {"users": [], "emoji": "🟡"},
            "dnd": {"users": [], "emoji": "🔴"},
            "offline": {"users": [], "emoji": "⚫"}
        }

        for user in ctx.guild.members:
            user_perm = ctx.channel.permissions_for(user)
            if user_perm.kick_members or user_perm.ban_members:
                if not user.bot:
                    all_status[str(user.status)]["users"].append(f"**{user}**")

        for g in all_status:
            if all_status[g]["users"]:
                message += f"{all_status[g]['emoji']} {', '.join(all_status[g]['users'])}\n"

        await ctx.send(f"Mods in **{ctx.guild.name}**\n{message}")
    
    # @commands.command(aliases=['startuptime', 'uptime'])
    # async def botstats(self, ctx):
    #     uptime = datetime.datetime.utcnow() - self.bot.uptime
    #     days = math.floor(uptime.days)
    #     seconds = math.floor(uptime.seconds)
    #     uptime = uptime.seconds
    #     hours = math.floor(uptime / 3600)
    #     minutes = math.floor(uptime / 60)
    #     embed = discord.Embed(
    #       title='Bot Statistics:',
    #       description=f'__Uptime:__\n{days}d {hours}h {minutes}m {seconds}s\n__Startup time:__\n{self.bot.startuptime.seconds}s'
    #     )
    #     await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Utilitys(bot))
