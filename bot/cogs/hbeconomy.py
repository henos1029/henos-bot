from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import discord
import random
import tools
import henostools
import replit
import aiosqlite

red = discord.Colour.red()


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # economy
    @commands.command(name='balance', aliases=['bal'])
    async def balance(self, ctx, user: discord.Member = None):
        'Shows your balance'
        if user == None:
            user = ctx.author
        await tools.open_account(user.id)
        db = await aiosqlite.connect('database.db')
        cur = await db.execute(f'SELECT wallet, bank FROM balance WHERE user=?', (user.id,))
        bal = await cur.fetchone()
        embed = discord.Embed(
            title=f"{user.name}'s balance",
            description=f'__Wallet:__ {bal[0]}\n__Bank:__ {bal[1]}')
        await ctx.send(embed=embed)
        await db.close()

    @commands.command()
    @commands.cooldown(1, 60, BucketType.user)
    async def beg(self, ctx):
        'begs for money'
        await tools.open_account(ctx.author.id)
        gain = random.randrange(100, 500)
        await ctx.send(f'Someone gave you {gain} dollars')
        await tools.save(user=ctx.author.id, amount=gain)

    @commands.command()
    @commands.cooldown(1, 86400, BucketType.user)
    async def daily(self, ctx):
        'get your daily dollars'
        await tools.open_account(ctx.author.id)
        gain = 3000
        await ctx.send(f'You got {gain} dollars as your daily dollars')
        await tools.save(user=ctx.author.id, amount=gain)

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amount):
        'deposits money into your bank'
        await tools.open_account(ctx.author.id)
        db = await aiosqlite.connect('database.db')
        cur = await db.execute('SELECT wallet,bank FROM balance WHERE user=?', (ctx.author.id,))
        rows = await cur.fetchone()
        wallet = rows[0]
        bank = rows[1]
        await db.close()
        del db
        if amount == 'all':
                await ctx.send(f'You deposited {wallet} dollars into your bank'
                               )
                db = await aiosqlite.connect('database.db')
                await db.execute('UPDATE balance SET wallet=wallet-wallet, bank=bank+wallet WHERE user=?', (ctx.author.id,))
                await db.commit()
                await db.close()
                del db
        else:
            if int(wallet) >= int(amount):
                await ctx.send(
                    f'You deposited {amount} dollars into your bank account')
                db = await aiosqlite.connect('database.db')
                await db.execute('UPDATE balance SET wallet=wallet-?, bank=bank+? WHERE user=?', (amount, amount, ctx.author.id,))
                await db.commit()
                await db.close()
                del db
            else:
                await ctx.send("You don't have enough money in your wallet")

    @commands.command(aliases=['with'])
    async def withdraw(self, ctx, amount):
        'withdraw money'
        db = await aiosqlite.connect('database.db')
        cur = await db.execute('SELECT wallet,bank FROM balance WHERE user=?', (ctx.author.id,))
        rows = await cur.fetchone()
        wallet = rows[0]
        bank = rows[1]
        await db.close()
        del db
        if amount <= int(bank):
            if amount == 'all':
                await ctx.send(
                    f'You withdrawed {bank} dollars from your bank')
                db = await aiosqlite.connect('database.db')
                await db.execute('UPDATE balance SET wallet=wallet+bank, bank=bank-bank WHERE user=?', (ctx.author.id,))
                await db.commit()
                await db.close()
                del db
            else:
                await ctx.send(
                    f'You withdrawed {amount} dollars from your bank account')
                db = await aiosqlite.connect('database.db')
                await db.execute('UPDATE balance SET wallet=wallet+?, bank=bank-? WHERE user=?', (amount, amount, ctx.author.id,))
                await db.commit()
                await db.close()
                del db
        else:
            await ctx.send("You don't have enough money in you bank account")

    @commands.command()
    @commands.cooldown(1, 3600, BucketType.user)
    async def work(self, ctx):
        'work as a random job'
        await tools.open_account(ctx.author.id)
        jobs = [
            'Janitor', 'Computer Programmer', 'Landscape Architect', 'Referee',
            'Teacher', 'Security Guard', 'Truck Driver', 'Plumber', 'Reporter',
            'Dancer', 'Vet', 'Chef', 'Childcare worker', 'Mason',
            'Electrician', 'Librarian', 'Writer', 'Bus Driver', 'Artist',
            'Accountant', 'CEO'
        ]
        gain = random.randrange(100, 5000)
        await tools.save(user=ctx.author.id, amount=gain)
        embed = discord.Embed(
            title=f'{ctx.author.name} worked!',
            description=
            f'You worked as a {random.choice(jobs)} and got {gain} dollars')
        embed.set_footer(text='Well done!! 👏')
        await ctx.send(embed=embed)

    @commands.command(aliases=['helping_hand'])
    @commands.cooldown(1, 60, BucketType.user)
    async def hh(self, ctx):
        'lend a helping hand'
        await tools.open_account(ctx.author.id)
        gain = random.randrange(10, 500)
        await ctx.send(f'You helped someone and got {gain} dollars in return')
        await tools.save(user=ctx.author.id, amount=gain)

    @commands.command()
    @commands.cooldown(1, 60, BucketType.user)
    async def search(self, ctx):
        'search somewhere'
        await tools.open_account(ctx.author.id)
        c1 = ['bed', 'discord', 'tree', 'street']
        c2 = [
            'car',
            'bed',
            'wallet',
            'pantry',
        ]
        c3 = ['shop', 'bushes', 'bin']
        choices = [random.choice(c1), random.choice(c2), random.choice(c3)]
        await ctx.send(
            f'Where do you want to search? Pick from the list below and type it in chat.\n`{choices[0]}, {choices[1]}, {choices[2]}`'
        )

        def search_check(msg):
            return msg.content in choices and msg.author.id == ctx.author.id

        msg = await self.bot.wait_for('message', check=search_check)
        amount = random.randrange(100, 500)
        if msg:
            await tools.save(user=ctx.author.id, amount=amount)
            await ctx.send(
                f'{ctx.author.mention}  **Searched the:** `{msg.content}`\nYou found {amount} dollars!'
            )
        else:
            if msg.author.id == ctx.author.id:
                await ctx.send('thats not a valid option')

    @commands.command()
    @commands.cooldown(1, 3600, BucketType.user)
    async def gamble(self, ctx, amount: int):
        'gamble money'
        await tools.open_account(ctx.author.id)
        db = await aiosqlite.connect('database.db')
        cur = await db.execute('SELECT wallet,bank FROM balance WHERE user=?', (ctx.author.id,))
        rows = await cur.fetchone()
        wallet = rows[0]
        bank = rows[1]
        await db.close()
        if int(wallet) >= amount:
            chance = ['win', 'lose']
            chance = random.choice(chance)
            em1 = discord.Embed(
                title=f"{ctx.author.name}'s gambling game!!",
                description='Will you win?')
            msg = await ctx.send(embed=em1)
            await henostools.sleep('2s')
            await msg.delete()
            msg2 = await ctx.send('Rolling now ...')
            if chance == 'win':
                amount2 = amount + 500
                gain = random.randrange(amount, amount2)
                await tools.save(user=ctx.author.id, amount=gain)
                await msg2.edit(
                    content=f'You Won!!\n\nYou got {gain} dollars!!')
            else:
                amount2 = amount + 500
                gain = random.randrange(amount, amount2)
                db = await aiosqlite.connect('database.db')
                await db.execute('UPDATE balance SET wallet=wallet-? WHERE user=?', (gain, ctx.author.id,))
                await db.commit()
                await db.close()
                await msg2.edit(
                    content=
                    f'You lost ):\n\n{gain} dollars was removed from your account'
                )
        else:
            await ctx.send("You don't have enough money. Please try again")

    @commands.command()
    @commands.cooldown(1, 3600, BucketType.user)
    async def lottery(self, ctx):
        'enter the lottery'
        await tools.open_account(ctx.author.id)
        db = await aiosqlite.connect('database.db')
        cur = await db.execute('SELECT wallet,bank FROM balance WHERE user=?', (ctx.author.id,))
        rows = await cur.fetchone()
        wallet = rows[0]
        bank = rows[1]
        await db.close()
        await ctx.send(
            'Are you sure you want to enter the lottery??\nEnter `yes` or `no`'
        )

        def lottcheck(msg):
            return msg.content.lower(
            ) == 'yes' and msg.author.id == ctx.author.id

        msg = await self.bot.wait_for('message', check=lottcheck)
        if msg:
            db = await aiosqlite.connect('database.db')
            await db.execute('UPDATE balance SET wallet=wallet-? WHERE user=?', (100, ctx.author.id,))
            await db.commit()
            await db.close()
            amount = random.randrange(100000, 2000000)
            chance = random.randrange(1, 2000)
            await ctx.send('Drumroll please ...')
            await henostools.sleep('10s')
            if chance == 100:
                await ctx.send(
                    f'Congrats!!!\n\nYou won the lottery and got {amount} dollars'
                )
                await tools.save(user=ctx.author.id, amount=amount)
            else:
                await ctx.send(
                    'Sooo close!!\nPlay again for the chance to win over 2 million dollars!!'
                )
        else:
            await ctx.send('Invaild Response.')

    @commands.command(aliases=['store'])
    async def shop(self, ctx):
        'see the shop'
        colours = discord.Embed(
            title='Colours',
            description=
            'Every colour costs `50,000`\n**Colours:**\n- `red`\n- `blue`\n- `green`\n- ` orange`\n- `pink`\n- `purple`\n- `gray`\n- `black`\nTo buy a role type `hb: buy colour <colour>`\n\nYou can also buy a custom colour for 100,000, use `hb:  buy customcolour <hexcode>`')
        await ctx.send(embed=colours)
        items = discord.Embed(
            title='Items',
            description=
            '- `Cookie` | 100 dollars\n- `Chocolate` | 500 dollars\n- `Coin` | 1,000 dollars\n- `Rare Coin` | 5,000 dollars\n- `Medal` | 10,000 dollars\n- `Rare Medal` | 50,000 dollars\n- `Trophy` | 100,000 dollars\n- `Rare Trophy` | 500,000 dollars\n- `Ultra Collectable Thingy` | 1,000,000 dollars\n\nUse `hb: buy item <item>`')
        await ctx.send(embed=items)

    @commands.group()
    async def buy(self, ctx):
        'buy an item/colour'
        if ctx.invoked_subcommand is None:
            await ctx.send(
                'Invalid catagory.\nExample: `hb: buy item Chocolate` (`hb: buy <catagory> <item>`)'
            )

    @buy.command()
    async def colour(self, ctx, *, colour):
        'buy a colour'
        await tools.open_account(ctx.author.id)
        role = discord.utils.get(ctx.guild.roles, name=colour)
        db = await aiosqlite.connect('database.db')
        cur = await db.execute('SELECT wallet,bank FROM balance WHERE user=?', (ctx.author.id,))
        rows = await cur.fetchone()
        wallet = rows[0]
        bank = rows[1]
        await db.close()
        if int(wallet) >= 50000:
            db = await aiosqlite.connect('database.db')
            await db.execute('UPDATE balance SET wallet=wallet-? WHERE user=?', (50000, ctx.author.id,))
            await db.commit()
            await db.close()
            await ctx.author.add_roles(role, reason='colour role add')
            await ctx.send(f'Gave you the colour {colour}!\nEnjoy!!')
        else:
            await ctx.send("You don't have enough money to buy this colour :(")

    @buy.command()
    async def item(self, ctx, *, item):
        'buy an item'
        await tools.open_account(ctx.author.id)
        item = item.lower()
        db = await aiosqlite.connect('database.db')
        cur = await db.execute('SELECT wallet,bank FROM balance WHERE user=?', (ctx.author.id,))
        rows = await cur.fetchone()
        wallet = rows[0]
        bank = rows[1]
        await db.close()
        if item == 'cookie':
            if int(wallet) >= tools.amounts.Cookie:
                await tools.remove(user=ctx.author.id, amount=tools.amounts.Cookie)
                itemdb = replit.db['Cookie']
                itemdb.append(ctx.author.id)
                replit.db['Cookie'] = itemdb
                await ctx.send('Congrats, You bought a Cookie')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        elif item == 'chocolate':
            if int(wallet) >= tools.amounts.Chocolate:
                await tools.remove(user=ctx.author.id, amount=tools.amounts.Chocolate)
                itemdb = replit.db['Chocolate']
                itemdb.append(ctx.author.id)
                replit.db['Chocolate'] = itemdb
                await ctx.send('Congrats, You bought a Chocolate')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        elif item == 'coin':
            if int(wallet) >= tools.amounts.Coin:
                await tools.remove(user=ctx.author.id, amount=tools.amounts.Coin)
                itemdb = replit.db['Coin']
                itemdb.append(ctx.author.id)
                replit.db['Coin'] = itemdb
                await ctx.send('Congrats, You bought a Coin')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        elif item == 'rare coin':
            if int(wallet) >= tools.amounts.RareCoin:
                await tools.remove(user=ctx.author.id, amount=tools.amounts.RareCoin)
                itemdb = replit.db['Rare Coin']
                itemdb.append(ctx.author.id)
                replit.db['Rare Coin'] = itemdb
                await ctx.send('Congrats, You bought a Rare Coin')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        elif item == 'medal':
            if int(wallet) >= tools.amounts.Medal:
                await tools.remove(user=ctx.author.id, amount=tools.amounts.Medal)
                itemdb = replit.db['Medal']
                itemdb.append(ctx.author.id)
                replit.db['Medal'] = itemdb
                await ctx.send('Congrats, You bought a Medal')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        elif item == 'rare medal':
            if int(wallet) >= tools.amounts.RareMedal:
                await tools.remove(user=ctx.author.id, amount=tools.amounts.RareMedal)
                itemdb = replit.db['Rare Medal']
                itemdb.append(ctx.author.id)
                replit.db['Rare Medal'] = itemdb
                await ctx.send('Congrats, You bought a Rare Medal')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        elif item == 'trophy':
            if int(wallet) >= tools.amounts.Trophy:
                await tools.remove(user=ctx.author.id, amount=tools.amounts.Trophy)
                itemdb = replit.db['Trophy']
                itemdb.append(ctx.author.id)
                replit.db['Trophy'] = itemdb
                await ctx.send('Congrats, You bought a Trophy')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        elif item == 'rare trophy':
            if int(wallet) >= tools.amounts.RareTrophy:
                await tools.remove(user=ctx.author.id, amount=tools.amounts.RareTrophy)
                itemdb = replit.db['Rare Trophy']
                itemdb.append(ctx.author.id)
                replit.db['Rare Trophy'] = itemdb
                await ctx.send('Congrats, You bought a Rare Trophy')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        elif item == 'ultra collectable thingy':
            if int(wallet) >= tools.amounts.UltraCollectableThingy:
                await tools.remove(user=ctx.author.id, amount=tools.amounts.UltraCollectableThingy)
                itemdb = replit.db['Ultra Collectable Thingy']
                itemdb.append(ctx.author.id)
                replit.db['Ultra Collectable Thingy'] = itemdb
                await ctx.send(
                    'Congrats, You bought a Ultra Collectable Thingy')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        else:
            await ctx.send('invalid item')

    @buy.command()
    async def customcolour(self, ctx, colour : discord.Colour):
        'buy a custom colour'
        await tools.open_account(ctx.author.id)
        db = await aiosqlite.connect('database.db')
        cur = await db.execute('SELECT wallet,bank FROM balance WHERE user=?', (ctx.author.id,))
        rows = await cur.fetchone()
        wallet = rows[0]
        bank = rows[1]
        await db.close()
        if int(wallet) >= 100000:
            await tools.remove(user=ctx.author.id, amount=100000)
            role = await ctx.guild.create_role(
                name=f'{ctx.author.name} - {colour}', colour=colour)
            await ctx.author.add_roles(role, reason='custom colour role add')
            await ctx.send(f'Gave you the colour {colour}\nEnjoy!!')
        else:
            await ctx.send("You don't have enough money to buy this :(")

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx, member: discord.Member = None):
        'see your inventory'
        if member == None:
            member = ctx.author
        Cookie = 0
        Chocolate = 0
        Coin = 0
        RareCoin = 0
        Medal = 0
        RareMedal = 0
        Trophy = 0
        RareTrophy = 0
        UltraCollectableThingy = 0
        CookieCheck = replit.db['Cookie']
        ChocolateCheck = replit.db['Chocolate']
        CoinCheck = replit.db['Coin']
        RareCoinCheck = replit.db['Rare Coin']
        MedalCheck = replit.db['Medal']
        RareMedalCheck = replit.db['Rare Medal']
        TrophyCheck = replit.db['Trophy']
        RareTrophyCheck = replit.db['Rare Trophy']
        UltraCollecableThingyCheck = replit.db['Ultra Collectable Thingy']
        for user in CookieCheck:
            if user == member.id:
                Cookie += 1
        for user in ChocolateCheck:
            if user == member.id:
                Chocolate += 1
        for user in CoinCheck:
            if user == member.id:
                Coin += 1
        for user in RareCoinCheck:
            if user == member.id:
                RareCoin += 1
        for user in MedalCheck:
            if user == member.id:
                Medal += 1
        for user in RareMedalCheck:
            if user == member.id:
                RareMedal += 1
        for user in TrophyCheck:
            if user == member.id:
                Trophy += 1
        for user in RareTrophyCheck:
            if user == member.id:
                RareTrophy += 1
        for user in UltraCollecableThingyCheck:
            if user == member.id:
                UltraCollectableThingy += 1

        embed = discord.Embed(
                title=f"{member.name}'s inventory",
                description=
                f"Cookie: {Cookie}\nChocholate: {Chocolate}\nCoin: {Coin}\nRare Coin: {RareCoin}\nMedal: {Medal}\nMedal: {RareMedal}\nRare Medal: {RareMedal}\nTrophy: {Trophy}\nRare Trophy: {RareTrophy}\nUltra Collectable Thingy: {UltraCollectableThingy}")
        await ctx.send(embed=embed)
    
    @commands.command(hidden=True, aliases=['claim', 'claimcool'])
    @commands.cooldown(1, 86400, BucketType.user)
    async def coolclaim(self, ctx):
        if ctx.author.id in tools.cool_people:
            await ctx.channel.purge(limit=1)
            gain = random.randrange(1000, 100000)
            await tools.save(user=ctx.author.id, amount=gain)
            msg = await ctx.send(f'You got {gain} dollars for being cool')
            await henostools.sleep('5s')
            await msg.delete()
        else:
            await ctx.send('You are not cool enough to use this command')
    
    @commands.command()
    async def rob(self, ctx, user : discord.Member):
        await tools.open_account(ctx.author.id)
        await tools.open_account(user.id)
        db = self.bot.db
        cur = await db.execute('SELECT wallet,bank FROM balance WHERE user=?', (ctx.author.id,))
        rows = await cur.fetchone()
        wallet = rows[0]
        bank = rows[1]
        await db.close()
        db = self.bot.db
        cur = await db.execute('SELECT wallet,bank FROM balance WHERE user=?', (user.id,))
        rows = await cur.fetchone()
        wallet2 = rows[0]
        bank2 = rows[1]
        await db.close()
        robamt = random.randrange(0, int(wallet))
        db = await aiosqlite.connect('database.db')
        await db.execute('UPDATE balance SET wallet=wallet+?, WHERE user=?', (robamt, ctx.author.id,))
        await db.commit()
        await db.close()
        db = await aiosqlite.connect('database.db')
        await db.execute('UPDATE balance SET wallet=wallet-?, WHERE user=?', (robamt, user.id,))
        await db.commit()
        await db.close()
        wallet = int(wallet)
        await ctx.send(f'You stole {robamt} from {user.mention}!!')
    
    @commands.command(aliases=['slots'])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"
        wingain = random.randrange(100, 1000)
        twogain = random.randrange(50, 500)
        if (a == b == c):
            await tools.save(user=ctx.author.id, amount=wingain)
            await ctx.send(f"{slotmachine} All matching, you won {wingain} dollars! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await tools.save(user=ctx.author.id, amount=twogain)
            await ctx.send(f"{slotmachine} 2 in a row, you won {twogain} dollars! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")
    
    @commands.command()
    async def leaderboard(self, ctx):
      db = await aiosqlite.connect('database.db')
      lb = await db.execute('SELECT user,wallet FROM balance ORDER BY wallet DESC LIMIT 5')
      no1 = lb[0]
      no2 = lb[1]
      no3 = lb[2]
      no4 = lb[3]
      no5 = lb[4]
      embed = discord.Embed(
        title='henos bot leaderboard',
        description=f'''1: <@{no1[0]}> - {no1[1]}
        2: <@{no2[0]}> - {no2[1]}
        3: <@{no3[0]}> - {no3[1]}
        4: <@{no4[0]}> - {no4[1]}
        5: <@{no5[0]}> - {no5[1]}
        '''
      )
      embed.set_footer(text='Leaderboard is done by balance')
      await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Economy(bot))
