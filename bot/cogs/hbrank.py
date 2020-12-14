rom discord.ext import commands
import discord
import tools
import aiosqlite

red = discord.Colour.red()


class rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rank(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        await tools.open_account(user.id)
        db = await aiosqlite.connect('database.db')
        cur = await db.execute(f'SELECT xp, level FROM levels WHERE user=?', (user.id,))
        rank = await cur.fetchone()
        embed = discord.Embed(
            title=f"{user.name}'s rank",
            description=f'__XP:__ {rank[0]}\n__Level:__ {rank[1]}')
        await ctx.send(embed=embed)
        await db.close()


def setup(bot):
    bot.add_cog(rank(bot))
