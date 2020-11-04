from discord.ext import commands
import discord

red = discord.Colour.red()


class moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1000):
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(
            title='__Clear!__',
            description=
            f'{ctx.author.mention}, I have cleared some messages for you',
            colour=red)
        embed.set_footer(text='Deleting in 30 seconds')
        await ctx.send(embed=embed, delete_after=30)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embed = discord.Embed(
            title='__Ban!__',
            description=
            f'{member.name}#{member.discriminator} was banned from {member.guild.name}',
            colour=red)
        embed.set_footer(text=f'Reason: {reason}')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        embed = discord.Embed(
            title='__Kick!__',
            description=
            f'{member.name}#{member.discriminator} was kicked from {member.guild.name}',
            colour=red)
        embed.set_footer(text=f'Reason: {reason}')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        unbanned_member = discord.Object(id=int(member.id))
        await member.unban(unbanned_member)
        embed = discord.Embed(
            title='__Unban!__',
            description=
            '{member.name}#{member.discriminator} was unbaned from {member.guild.name}',
            colour=red)
        embed.set_footer(text='They can now rejoin!!')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(moderation(bot))
