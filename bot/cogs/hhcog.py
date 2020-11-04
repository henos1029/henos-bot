import discord
from discord.ext import commands
import tools
from replit import db

red = discord.Colour.red()


class h_helper(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def add_wallet(self, ctx, user: discord.Member, amount: int):
        'adds money to someones wallet'
        await tools.open_account(user.id)
        await tools.save(user=user.id, amount=amount)
        await ctx.send(f"Added {amount} to {user.mention}'s wallet")

    @commands.command()
    @commands.is_owner()
    async def add_bank(self, ctx, user: discord.Member, amount: int):
        'adds money to someones bank'
        await tools.open_account(user.id)
        wallet, bank, xp, level = db[user.id].split(',')
        db[user] = f'{wallet},{int(bank) + amount},{xp},{level}'
        await ctx.send(f"Added {amount} to {user.mention}'s bank")

    @commands.command()
    @commands.is_owner()
    async def add_xp(self, ctx, user: discord.Member, amount: int):
        'adds xp to someones xp'
        await tools.open_account(user.id)
        wallet, bank, xp, level = db[user.id].split(',')
        db[user] = f'{wallet},{bank},{int(xp) + amount},{level}'
        await ctx.send(f"Added {amount} to {user.mention}'s xp")

    @commands.command()
    @commands.is_owner()
    async def add_level(self, ctx, user: discord.Member, amount: int):
        'adds a level to someones level'
        await tools.open_account(user.id)
        wallet, bank, xp, level = db[user.id].split(',')
        db[user] = f'{wallet},{bank},{xp},{int(level) + amount}'
        await ctx.send(f"Added {amount} to {user.mention}'s level")

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(
            title="__Pong__",
            description=f'{round(self.bot.latency * 1000)} ms',
            colour=red)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def del_key(ctx):
        del db[ctx.author.id]
        await ctx.send('Done!')

    @commands.command(name='initialize', aliases=['init'])
    @commands.is_owner()
    async def initialize_stuff(self, ctx):
        return
        # items = [
        #     'Cookie', 'Chocolate', 'Coin', 'Rare Coin', 'Medal', 'Rare Medal',
        #     'Trophy', 'Rare Trophy', 'Ultra Collectable Thingy'
        # ]
        # for item in items:
        #     del db[item]
        #     await ctx.send(f'Deleted shop item {item}.')
        # for item in items:
        #     db[item] = []
        # for item in items:
        #     item2 = db[item]
        #     item2.append(ctx.author.id)
        #     db[item] = item2
        #     await ctx.send(f'Created shop item {item} and gave it to you.')


def setup(bot):
    bot.add_cog(h_helper(bot))
