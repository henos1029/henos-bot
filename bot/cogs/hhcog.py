import discord
from discord.ext import commands
import tools
from replit import db
import aiosqlite

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
        db = await aiosqlite.connect('database.db')
        await db.execute(f'UPDATE balance SET bank = bank+? WHERE user=?', (amount, user))
        await db.commit()
        await db.close()
        await ctx.send(f"Added {amount} to {user.mention}'s bank")

    @commands.command()
    @commands.is_owner()
    async def add_xp(self, ctx, user: discord.Member, amount: int):
        'adds xp to someones xp'
        await tools.open_account(user.id)
        db = await aiosqlite.connect('database.db')
        await db.execute(f'UPDATE levels SET xp = xp+? WHERE user=?', (amount, user))
        await db.commit()
        await db.close()
        await ctx.send(f"Added {amount} to {user.mention}'s xp")

    @commands.command()
    @commands.is_owner()
    async def add_level(self, ctx, user: discord.Member, amount: int):
        'adds a level to someones level'
        await tools.open_account(user.id)
        db = await aiosqlite.connect('database.db')
        await db.execute(f'UPDATE levels SET level = level+? WHERE user=?', (amount, user))
        await db.commit()
        await db.close()
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
        # return
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
        # db['Ignored'] = [374071874222686211]
        # await ctx.send('Created var Ignored')
        # db[ctx.author.id] = '9043,506995,24,97'
        # await ctx.send('done!')
        items = [
            'Cookie', 'Chocolate', 'Coin', 'Rare Coin', 'Medal', 'Rare Medal',
            'Trophy', 'Rare Trophy', 'Ultra Collectable Thingy', 'Ignored', ctx.author.id
        ]
        dicty = {}
        for item in items:
           dicty[item] = db[item]
        # for key in db.keys():
        #   del key
        # await ctx.send(dicty)
        db['Ignored'] = [374071874222686211, 336642139381301249]
        dicty['Ignored'] = db['Ignored']
        await ctx.send(f'done\n{dicty}')
        return

    @commands.command()
    async def verify(self, ctx):
      await ctx.message.delete()
      await ctx.send(f'{ctx.author.mention}, please check you dms.', delete_after=30)
      await ctx.author.send(f'Verification Process has started...\n\nPlease enter your username and discriminator to verify your account.\ne.g.: `henos bot#2743`')
      def verifycheck(msg):
        return msg.content == str(ctx.author)
      msg = await self.bot.wait_for('message', check=verifycheck)
      if msg:
        await ctx.author.send('You have successfuly verified your account, head back to `henos\'s bots` to start chatting')
        await ctx.author.add_roles(ctx.guild.get_role(778556601580912640))
      else:
        await ctx.author.send('Incorrect response, please run the command again')
    
    @commands.command()
    @commands.is_owner()
    async def sql(self, ctx, query):
      query = tools.cleanup_code(query)

def setup(bot):
    bot.add_cog(h_helper(bot))
