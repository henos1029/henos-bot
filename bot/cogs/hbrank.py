from discord.ext import commands
import discord
import tools
from replit import db

red = discord.Colour.red()


class rank(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def rank(self, ctx, user: discord.Member = None):
        if user == None:
            await tools.open_account(ctx.author.id)
            wallet, bank, xp, level = db[ctx.author.id].split(',')
            embed = discord.Embed(
                title=f"{ctx.author.name}'s rank",
                description=f'__XP:__ {xp}\n__Level:__ {level}',
                colour=red)
            await ctx.send(embed=embed)
        else:
            await tools.open_account(user.id)
            wallet, bank, xp, level = db[user.id].split(',')
            embed = discord.Embed(
                title=f"{user.name}'s rank",
                description=f'__XP:__ {xp}\n__Level:__ {level}',
                colour=red)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(rank(bot))
