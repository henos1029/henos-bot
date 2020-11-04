from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import discord
import random
import tools
import henostools
from replit import db

red = discord.Colour.red()


class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # economy
    @commands.command(name='balance', aliases=['bal'])
    async def balance(self, ctx, user: discord.Member = None):
        'Shows your balance'
        if user == None:
            await tools.open_account(ctx.author.id)
            wallet, bank, xp, level = db[ctx.author.id].split(',')
            embed = discord.Embed(
                title=f"{ctx.author.name}'s balance",
                description=f'__Wallet:__ {wallet}\n__Bank:__ {bank}',
                colour=red)
            await ctx.send(embed=embed)
        else:
            await tools.open_account(user.id)
            wallet, bank, xp, level = db[user.id].split(',')
            embed = discord.Embed(
                title=f"{user.name}'s balance",
                description=f'__Wallet:__ {wallet}\n__Bank:__ {bank}',
                colour=red)
            await ctx.send(embed=embed)

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
        await tools.save(user=str(ctx.author.id), amount=gain)

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amount: int):
        'deposits money into your bank'
        await tools.open_account(ctx.author.id)
        wallet, bank, xp, level = db[ctx.author.id].split(',')
        if int(amount) <= int(wallet):
            if amount == 'all':
                await ctx.send(f'You deposited {wallet} dollars into your bank'
                               )
                db[ctx.author.
                   id] = f'{str(int(wallet) - int(wallet))},{str(int(bank) + int(wallet))},{xp},{level}'
            else:
                await ctx.send(
                    f'You deposited {amount} dollars into your bank account')
                db[ctx.author.
                   id] = f'{str(int(wallet) - amount)},{str(int(bank) + amount)},{xp},{level}'
        else:
            await ctx.send("You don't have enough money in your wallet")

    @commands.command(aliases=['with'])
    async def withdraw(self, ctx, amount: int):
        'withdraw money'
        wallet, bank, xp, level = db[ctx.author.id].split(',')
        if amount <= int(bank):
            if amount == 'all':
                await ctx.send(
                    f'You withdrawed {wallet} dollars from your bank')
                db[ctx.author.
                   id] = f'{str(int(wallet) + int(bank))},{str(int(bank) - int(bank))},{xp},{level}'
            else:
                await ctx.send(
                    f'You withdrawed {amount} dollars from your bank account')
                db[ctx.author.
                   id] = f'{str(int(wallet) + int(amount))},{str(int(bank) - int(amount))},{xp},{level}'
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
        await tools.save(user=str(ctx.author.id), amount=gain)
        embed = discord.Embed(
            title=f'{ctx.author.name} worked!',
            description=
            f'You worked as a {random.choice(jobs)} and got {gain} dollars',
            colour=red)
        embed.set_footer(text='Well done!! 👏')
        await ctx.send(embed=embed)

    @commands.command(aliases=['helping_hand'])
    @commands.cooldown(1, 60, BucketType.user)
    async def hh(self, ctx):
        'lend a helping hand'
        await tools.open_account(ctx.author.id)
        gain = random.randrange(10, 500)
        await ctx.send(f'You helped someone and got {gain} dollars in return')
        await tools.save(user=str(ctx.author.id), amount=gain)

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
        wallet, bank, xp, level = db[ctx.author.id].split(',')
        if int(wallet) >= amount:
            chance = ['win', 'lose']
            chance = random.choice(chance)
            em1 = discord.Embed(
                title=f"{ctx.author.name}'s gambling game!!",
                description='Will you win?',
                colour=red)
            msg = await ctx.send(embed=em1)
            await henostools.sleep('2s')
            await msg.delete()
            msg2 = await ctx.send('Rolling now ...')
            if chance == 'win':
                amount2 = amount + 500
                gain = random.randrange(amount, amount2)
                db[ctx.author.id] = f'{int(wallet) + gain},{bank},{xp},{level}'
                await msg2.edit(
                    content=f'You Won!!\n\nYou got {gain} dollars!!')
            else:
                amount2 = amount + 500
                gain = random.randrange(amount, amount2)
                db[ctx.author.id] = f'{int(wallet) - gain},{bank},{xp},{level}'
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
        wallet, bank, xp, level = db[ctx.author.id].split(',')
        await ctx.send(
            'Are you sure you want to enter the lottery??\nEnter `yes` or `no`'
        )

        def lottcheck(msg):
            return msg.content.lower(
            ) == 'yes' and msg.author.id == ctx.author.id

        msg = await self.bot.wait_for('message', check=lottcheck)
        if msg:
            db[ctx.author.id] = f'{int(wallet) - 100},{bank},{xp},{level}'
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
            'Every colour costs `50,000`\n**Colours:**\n- `red`\n- `blue`\n- `green`\n- ` orange`\n- `pink`\n- `purple`\n- `gray`\n- `black`\nTo buy a role type `hb: buy colour <colour>`\n\nYou can also buy a custom colour for 100,000, use `hb:  buy customcolour <hexcode>`',
            colour=red)
        await ctx.send(embed=colours)
        items = discord.Embed(
            title='Items',
            description=
            '- `Cookie` | 100 dollars\n- `Chocolate` | 500 dollars\n- `Coin` | 1,000 dollars\n- `Rare Coin` | 5,000 dollars\n- `Medal` | 10,000 dollars\n- `Rare Medal` | 50,000 dollars\n- `Trophy` | 100,000 dollars\n- `Rare Trophy` | 500,000 dollars\n- `Ultra Collectable Thingy` | 1,000,000 dollars\n\nUse `hb: buy item <item>`',
            colour=red)
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
        wallet, bank, xp, level = db[ctx.author.id].split(',')
        if int(wallet) >= 50000:
            db[ctx.author.id] = f'{int(wallet) - 50000},{bank},{xp},{level}'
            await ctx.author.add_roles(role, reason='colour role add')
            await ctx.send(f'Gave you the colour {colour}!\nEnjoy!!')
        else:
            await ctx.send("You don't have enough money to buy this colour :(")

    @buy.command()
    async def item(self, ctx, *, item):
        'buy an item'
        await tools.open_account(ctx.author.id)
        item = item.lower()
        wallet, bank, xp, level = db[ctx.author.id].split(',')
        if item == 'cookie':
            if int(wallet) >= tools.amounts.Cookie:
                db[ctx.author.
                   id] = f'{int(wallet) - tools.amounts.Cookie},{bank},{xp},{level}'
                itemdb = db['Cookie']
                itemdb.append(ctx.author.id)
                db['Cookie'] = itemdb
                await ctx.send('Congrats, You bought a Cookie')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        elif item == 'chocolate':
            if int(wallet) >= tools.amounts.Chocolate:
                db[ctx.author.
                   id] = f'{int(wallet) - tools.amounts.Chocolate},{bank},{xp},{level}'
                itemdb = db['Chocolate']
                itemdb.append(ctx.author.id)
                db['Chocolate'] = itemdb
                await ctx.send('Congrats, You bought a Chocolate')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        elif item == 'coin':
            if int(wallet) >= tools.amounts.Coin:
                db[ctx.author.
                   id] = f'{int(wallet) - tools.amounts.Coin},{bank},{xp},{level}'
                itemdb = db['Coin']
                itemdb.append(ctx.author.id)
                db['Coin'] = itemdb
                await ctx.send('Congrats, You bought a Coin')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        elif item == 'rare coin':
            if int(wallet) >= tools.amounts.RareCoin:
                db[ctx.author.
                   id] = f'{int(wallet) - tools.amounts.RareCoin},{bank},{xp},{level}'
                itemdb = db['Rare Coin']
                itemdb.append(ctx.author.id)
                db['Rare Coin'] = itemdb
                await ctx.send('Congrats, You bought a Rare Coin')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        elif item == 'medal':
            if int(wallet) >= tools.amounts.Medal:
                db[ctx.author.
                   id] = f'{int(wallet) - tools.amounts.Medal},{bank},{xp},{level}'
                itemdb = db['Medal']
                itemdb.append(ctx.author.id)
                db['Medal'] = itemdb
                await ctx.send('Congrats, You bought a Medal')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        elif item == 'rare medal':
            if int(wallet) >= tools.amounts.RareMedal:
                db[ctx.author.
                   id] = f'{int(wallet) - tools.amounts.RareMedal},{bank},{xp},{level}'
                itemdb = db['Rare Medal']
                itemdb.append(ctx.author.id)
                db['Rare Medal'] = itemdb
                await ctx.send('Congrats, You bought a Rare Medal')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        elif item == 'trophy':
            if int(wallet) >= tools.amounts.Trophy:
                db[ctx.author.
                   id] = f'{int(wallet) - tools.amounts.Trophy},{bank},{xp},{level}'
                itemdb = db['Trophy']
                itemdb.append(ctx.author.id)
                db['Trophy'] = itemdb
                await ctx.send('Congrats, You bought a Trophy')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        elif item == 'rare trophy':
            if int(wallet) >= tools.amounts.RareTrophy:
                db[ctx.author.
                   id] = f'{int(wallet) - tools.amounts.RareTrophy},{bank},{xp},{level}'
                itemdb = db['Rare Trophy']
                itemdb.append(ctx.author.id)
                db['Rare Trophy'] = itemdb
                await ctx.send('Congrats, You bought a Rare Trophy')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        elif item == 'ultra collectable thingy':
            if int(wallet) >= tools.amounts.UltraCollectableThingy:
                db[ctx.author.
                   id] = f'{int(wallet) - tools.amounts.UltraCollectableThingy},{bank},{xp},{level}'
                itemdb = db['Ultra Collectable Thingy']
                itemdb.append(ctx.author.id)
                db['Ultra Collectable Thingy'] = itemdb
                await ctx.send(
                    'Congrats, You bought a Ultra Collectable Thingy')
            else:
                await ctx.send(
                    "You don't have enough money to buy this item :(")
        else:
            await ctx.send('invalid item')

    @buy.command()
    async def customcolour(self, ctx, hexcode):
        'buy a custom colour'
        await tools.open_account(ctx.author.id)
        wallet, bank, xp, level = db[ctx.author.id].split(',')
        if int(wallet) >= 100000:
            db[ctx.author.id] = f'{int(wallet) - 100000},{bank},{xp},{level}'
            role = await ctx.guild.create_role(
                name=f'{ctx.author.name} - {hexcode}', colour=hexcode)
            await ctx.author.addroles(role, reason='custom colour role add')
            await ctx.send(f'Gave you the colour {hexcode}\nEnjoy!!')
        else:
            await ctx.send("You don't have enough money to buy this :(")

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx, member: discord.Member = None):
        'see your inventory'
        if member == None:
            Cookie = 0
            Chocolate = 0
            Coin = 0
            RareCoin = 0
            Medal = 0
            RareMedal = 0
            Trophy = 0
            RareTrophy = 0
            UltraCollectableThingy = 0
            CookieCheck = db['Cookie']
            ChocolateCheck = db['Chocolate']
            CoinCheck = db['Coin']
            RareCoinCheck = db['Rare Coin']
            MedalCheck = db['Medal']
            RareMedalCheck = db['Rare Medal']
            TrophyCheck = db['Trophy']
            RareTrophyCheck = db['Rare Trophy']
            UltraCollecableThingyCheck = db['Ultra Collectable Thingy']
            for user in CookieCheck:
                if user == ctx.author.id:
                    Cookie += 1
            for user in ChocolateCheck:
                if user == ctx.author.id:
                    Chocolate += 1
            for user in CoinCheck:
                if user == ctx.author.id:
                    Coin += 1
            for user in RareCoinCheck:
                if user == ctx.author.id:
                    RareCoin += 1
            for user in MedalCheck:
                if user == ctx.author.id:
                    Medal += 1
            for user in RareMedalCheck:
                if user == ctx.author.id:
                    RareMedal += 1
            for user in TrophyCheck:
                if user == ctx.author.id:
                    Trophy += 1
            for user in RareTrophyCheck:
                if user == ctx.author.id:
                    RareTrophy += 1
            for user in UltraCollecableThingyCheck:
                if user == ctx.author.id:
                    UltraCollectableThingy += 1

            embed = discord.Embed(
                title=f"{ctx.author.name}'s inventory",
                description=
                f"Cookie: {Cookie}\nChocholate: {Chocolate}\nCoin: {Coin}\nRare Coin: {RareCoin}\nMedal: {Medal}\nMedal: {RareMedal}\nRare Medal: {RareMedal}\nTrophy: {Trophy}\nRare Trophy: {RareTrophy}\nUltra Collectable Thingy: {UltraCollectableThingy}",
                colour=red)
            await ctx.send(embed=embed)
        else:
            Cookie = 0
            Chocolate = 0
            Coin = 0
            RareCoin = 0
            Medal = 0
            RareMedal = 0
            Trophy = 0
            RareTrophy = 0
            UltraCollectableThingy = 0
            CookieCheck = db['Cookie']
            ChocolateCheck = db['Chocolate']
            CoinCheck = db['Coin']
            RareCoinCheck = db['Rare Coin']
            MedalCheck = db['Medal']
            RareMedalCheck = db['Rare Medal']
            TrophyCheck = db['Trophy']
            RareTrophyCheck = db['Rare Trophy']
            UltraCollecableThingyCheck = db['Ultra Collectable Thingy']

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
                f"Cookie: {Cookie}\nChocholate: {Chocolate}\nCoin: {Coin}\nRare Coin: {RareCoin}\nMedal: {Medal}\nMedal: {RareMedal}\nRare Medal: {RareMedal}\nTrophy: {Trophy}\nRare Trophy: {RareTrophy}\nUltra Collectable Thingy: {UltraCollectableThingy}",
                colour=red)
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


def setup(bot):
    bot.add_cog(Economy(bot))
