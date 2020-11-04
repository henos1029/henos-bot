from discord.ext import commands  #, tasks
import discord
import random
import henostools
import pyshorteners

red = discord.Colour.red()


class fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # stuff
    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
            title='Invites:',
            description=
            'Bot: [tiny.cc/henosbot](https://tiny.cc/henos_bot)\nHelp Server: [tiny.cc/hb_help_server](https://tiny.cc/hb_help_server)',
            colour=red)
        await ctx.send(embed=embed)

    # fun
    @commands.command()
    async def poll(self, ctx, r1, r2, *, pollctx):
        embed = discord.Embed(
            title="__Poll!__", description=f'{pollctx}', colour=red)
        embed.set_footer(
            text=
            f'Poll by {ctx.author.name}#{ctx.author.discriminator} | React with {r1} or {r2} to vote'
        )
        message = await ctx.send(embed=embed)
        await ctx.message.delete()
        await message.add_reaction(r1)
        await message.add_reaction(r2)

    @commands.command()
    async def hack(self, ctx, user: discord.Member):
        ends = [
            'gmail.com', 'hotmail.com', 'outlook.com', 'optusnet.net',
            'bigpond.com'
        ]
        passends = ['is_cool', 'loves_chocolate', 'loves_itself']
        email = f'{user.name}{random.randrange(1000, 9999)}@{random.choice(ends)}'
        password = f'{user.name}{random.choice(passends)}{random.randrange(1000, 9999)}'
        embed = discord.Embed(
            title="__Hack Complete__",
            description=
            f"{user.mention}'s email: {email}\n{user.mention}'s Password: {password}",
            colour=red)
        message = await ctx.send(f'Hacking {user.mention} ...')
        await henostools.sleep('10s')
        await message.edit(embed=embed)

    @commands.command()
    async def giveaway(self, ctx, duration, *, prize):
        embed = discord.Embed(
            title='Giveaway!! 🎉',
            description=
            f'__**Prize**__: {prize}\n__**Duration**__: {duration}\n__**Hosted by**__: {ctx.author.mention}',
            colour=red)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('🎉')
        await henostools.sleep(duration)
        message = await ctx.channel.fetch_message(msg.id)
        choices = message.reactions
        winnerchoice = random.choice(choices)
        winner = winnerchoice.user
        embed2 = discord.Embed(
            title='Giveaway Ended',
            description=
            f'__**Winner**__: {winner.mention}\n__**Hosted by**__: {ctx.author.mention}',
            colour=red)
        await message.edit(embed=embed2)
        await ctx.send(
            f'Congrats {winner.mention}, you won {prize}\n\nhttps://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}\n({ctx.author.id})'
        )

    @commands.command()
    async def embedify(self, ctx, titletag, title, bodytag, body, footertag,
                       footer, colourtag, colour: int):
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(title=title, description=body, colour=colour)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)

    @commands.command()
    async def reactify(self, ctx, messageid: int, *, reactions: list):
        await ctx.channel.purge(limit=1)
        message = await ctx.channel.fetch_message(messageid)
        for reaction in reactions:
            await message.add_reaction(reaction)

    # ping
    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(
            title="__Pong__",
            description=f'{round(self.bot.latency * 1000)} ms',
            colour=red)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def shorten(self, ctx, *, link):
        msg = await ctx.send(f'Creating your short link for the url {link}')
        await henostools.sleep('2s')
        auth = pyshorteners.Shortener(api_key='28e1b34a-6095-485f-b912-41d3c5267578', login='HenoS')
        short_link = auth.tinycc.short(link)
        await msg.edit(text=f'Short link created: {short_link}')


def setup(bot):
    bot.add_cog(fun(bot))
