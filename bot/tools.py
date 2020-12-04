import json
import discord
import time
import traceback
from discord.ext import menus
import asyncio
import re
import aiosqlite

red = discord.Colour.red()

async def open_account(user):
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute('SELECT user FROM balance WHERE user=?', (user,))
    bal = await cursor.fetchone()
    await db.close()
    if bal is None:
        db = await aiosqlite.connect('database.db')
        await db.execute("INSERT INTO balance(user,wallet,bank) VALUES(?,?,?)", (user, 500, 0,))
        await db.commit()
        await db.close()
    db2 = await aiosqlite.connect('database.db')
    cursor2 = await db2.execute('SELECT user FROM levels WHERE user=?', (user,))
    level = await cursor2.fetchone()
    await db2.close()
    if level is None:
        db2 = await aiosqlite.connect('database.db')
        await db2.execute("INSERT INTO levels(user,xp,level) VALUES(?,?,?)", (user, 0, 0))
        await db2.commit()
        await db2.close()

async def save(user, amount: int):
    db = await aiosqlite.connect('database.db')
    await db.execute(f'UPDATE balance SET wallet = wallet+? WHERE user=?', (amount, user))
    await db.commit()
    await db.close()

async def remove(user, amount: int):
    db = await aiosqlite.connect('database.db')
    await db.execute(f'UPDATE balance SET wallet = wallet-? WHERE user=?', (amount, user))
    await db.commit()
    await db.close()

def premium(guild):
    with open('premium.json', 'r') as rf:
        premium = json.load(rf)
    if guild in premium:
        return True
    else:
        return False

def is_booster(member):
    if member in member.guild.premium_subscribers:
        return True
    else:
        return False

class amounts:
    Cookie = 100
    Chocolate = 500
    Coin = 1000
    RareCoin = 5000
    Medal = 10
    RareMedal = 50000
    Trophy = 100000
    RareTrophy = 500000
    UltraCollectableThingy = 1000000

cool_people = [717633235789807657, 766555259220787220, 727350727713882183, 775969041684234271]

helpdict = {
  1: discord.Embed(
          title='henos bot Help',
          description='''
          Key: <arg> - required argument, [arg] - optional argument
          Economy:
          `hb: balance [user]` - Shows you balance
          `hb: daily` - Get daily dollars
          `hb: work` - Work as a random job
          `hb: beg` - beg for dollars
          `hb: deposit/withdraw <amount>` - deposit/withdraw dollars
          `hb: search` - Search around for dollars
          `hb: hh` - Help someone
          `hb: gamble <amount>` - gamble your dollars
          `hb: lottery` - enter the lottery
          `hb: shop` - see the shop
          `hb: buy`
          |-`item <item>` - buys an item
          |-`colour <colour>` - buys a colour
          |_`customcolour <colour>` - buys a custom colour
          `hb: inventory [user]` - see your inventory
          ''',
          colour=red
        ),
  2: discord.Embed(
    title='henos bot Help',
    description='''
          Key: <arg> - required argument, [arg] - optional argument
          Fun:
          `hb: hack [user]` - Hacks someone
          `hb: invite` - Returns the invite link for the bot
          `hb: poll <reaction 1> <reaction 2> <message>` - Creates a poll
          `hb: giveaway <duration> <prize>` - Creates a giveaway
          `hb: embedify title: <title> body: <body> footer: <footer> colour: <colour>` - creates an embed with the fields specified
          `hb: reactify <message> <*reactions: list>` - adds reactions to the specified message
          `hb: ping` - returns the bot's ping
          `hb: kill [user]` - kills someone
          ''',
          colour=red
  ),
  3: discord.Embed(
    title='henos bot Help',
    description='''
          Key: <arg> - required argument, [arg] - optional argument
          Moderation:
          `hb: clear [amount=1000]` - Clears the specified amount of messages
          `hb: ban <user>` - bans a user
          `hb: unban <user>` - unbans a user
          `hb: kick <user>` - Kicks a user
          ''',
          colour=red
  ),
  4: discord.Embed(
    title='henos bot Help',
    description='''
          Key: <arg> - required argument, [arg] - optional argument
          Music:
          `hb: play <song>/stop` - Plays/stops a song
          `hb: join/leave` - joins/leaves the current vc
          `hb: pause/resume` - pauses/resumes the current songr
          `hb: queue` - Returns the current song queue
          `hb: shuffle` - Shuffles the current queue
          `hb: loop` - Loops the current song
          `hb: skip` - skips the current song
          `hb: now` - Returns the current playing song
          `hb: summon` - summons the bot to your vc
          ''',
          colour=red
  ),
  5: discord.Embed(
    title='henos bot Help',
    description='''
          Key: <arg> - required argument, [arg] - optional argument
          Rank:
          `hb: rank [user]` - Shows your rank
          ''',
          colour=red
  ),
  6: discord.Embed(
    title='henos bot Help',
    description='''
          Key: <arg> - required argument, [arg] - optional argument
          Utillitys:
          `hb: info [user]` - Shows info about you
          `hb: botinfo` - Shows info about the bot
          `hb: serverinfo` - Shows info about the server
          `hb: disableinteraction` - Disables all level-up and welcome messages
          ''',
          colour=red
  ),
  7: discord.Embed(
    title='henos bot Help',
    description='''
          Key: <arg> - required argument, [arg] - optional argument
          Image:
          `hb: filter` - appy a filter to an image
          |- `magik [user]` - magik version of the avatar
          |- `blur [user]` - blur version of the avatar
          |- `invert [user]` - invert version of the avatar
          |- `black_and_white [user]` - b&w version of the avatar
          |- `deepfry [user]` - deepfry version of the avatar
          |- `sepia [user]` - sepia version of the avatar
          |- `pixelate [user]` - pixetate version of the avatar
          |- `jpegify [user]` - jpegify version of the avatar
          |- `wide [user]` - wide version of the avatar
          |- `snow [user]` - snow version of the avatar
          |- `gay [user]` - gay version of the avatar
          |- `communist [user]` - communist version of the avatar
          |_ `random [user]` - random of the above
          `hb: trash [user]` - put a [user] in the trash
          `hb: ship <user>` - ship with a user
          `hb: salty [user]` - pour salt on a [user]
          `hb: amiajoke [user]` - asks if a [user] is a joke to you
          `hb: gradient <hexcolourcode>` - show a gradient of that colour
          `hb: calling <text>` - calls someone meme with that text
          ''',
          colour=red
  ),
}

colours = {
  '\U0001f534': 'Red',
  '\U0001f535': 'Blue',
  '\U0001f7e2': 'Green',
  '\U0001f7e0': 'Orange',
  '\U0001f7e3': 'Purple',
  '\U000026ab': 'Black',
  '\U00002755': 'Gray'
}
roles = {
  '\U0001f4fa': 'New YT Vid Ping',
  '\U00002620\U0000fe0f': 'Dead Chat Ping',
  '\U0001f4e3': 'Announcements Ping'
}

def date(target, clock=True):
    if not clock:
        return target.strftime("%d %B %Y")
    return target.strftime("%d %B %Y, %H:%M")

def timetext(name):
    return f"{name}_{int(time.time())}.txt"

def tracebacker(err, advance: bool = True):
    _traceback = ''.join(traceback.format_tb(err.__traceback__))
    error = ('```py\n{1}{0}: {2}\n```').format(type(err).__name__, _traceback, err)
    return error if advance else f"{type(err).__name__}: {err}"

class Pages(menus.MenuPages):
    def __init__(self, source):
        super().__init__(source=source, check_embeds=True)

    async def finalize(self, timed_out):
        try:
            if timed_out:
                await self.message.clear_reactions()
            else:
                await self.message.delete()
        except discord.HTTPException:
            pass

    @menus.button('\N{INFORMATION SOURCE}\ufe0f', position=menus.Last(3))
    async def show_help(self, payload):
        """shows this message"""
        embed = discord.Embed(title='Paginator help', description='Hello! Welcome to the help page.')
        messages = []
        for (emoji, button) in self.buttons.items():
            messages.append(f'{emoji}: {button.action.__doc__}')

        embed.add_field(name='What are these reactions for?', value='\n'.join(messages), inline=False)
        embed.set_footer(text=f'We were on page {self.current_page + 1} before this message.')
        await self.message.edit(content=None, embed=embed)

        async def go_back_to_current_page():
            await asyncio.sleep(30.0)
            await self.show_page(self.current_page)

        self.bot.loop.create_task(go_back_to_current_page())

    @menus.button('\N{INPUT SYMBOL FOR NUMBERS}', position=menus.Last(1.5))
    async def numbered_page(self, payload):
        """lets you type a page number to go to"""
        channel = self.message.channel
        author = self.message.author
        to_delete = []
        to_delete.append(await channel.send('What page do you want to go to?'))

        def message_check(m):
            return m.author == author and \
                   channel == m.channel and \
                   m.content.isdigit()

        try:
            msg = await self.bot.wait_for('message', check=message_check, timeout=30.0)
        except asyncio.TimeoutError:
            to_delete.append(await channel.send('Took too long.'))
            await asyncio.sleep(5)
        else:
            page = int(msg.content)
            to_delete.append(msg)
            await self.show_checked_page(page - 1)

        try:
            await channel.delete_messages(to_delete)
        except Exception:
            pass

class UrbanDictionaryPageSource(menus.ListPageSource):
    BRACKETED = re.compile(r'(\[(.+?)\])')
    def __init__(self, data):
        super().__init__(entries=data, per_page=1)

    def cleanup_definition(self, definition, *, regex=BRACKETED):
        def repl(m):
            word = m.group(2)
            return f'[{word}](http://{word.replace(" ", "-")}.urbanup.com)'

        ret = regex.sub(repl, definition)
        if len(ret) >= 2048:
            return ret[0:2000] + ' [...]'
        return ret

    async def format_page(self, menu, entry):
        maximum = self.get_max_pages()
        title = f'{entry["word"]}: {menu.current_page + 1} out of {maximum}' if maximum else entry['word']
        embed = discord.Embed(title=title, colour=0xE86222, url=entry['permalink'])
        embed.set_footer(text=f'by {entry["author"]}')
        embed.description = self.cleanup_definition(entry['definition'])

        try:
            up, down = entry['thumbs_up'], entry['thumbs_down']
        except KeyError:
            pass
        else:
            embed.add_field(name='Votes', value=f'\N{THUMBS UP SIGN} {up} \N{THUMBS DOWN SIGN} {down}', inline=False)

        try:
            date = discord.utils.parse_time(entry['written_on'][0:-1])
        except (ValueError, KeyError):
            pass
        else:
            embed.timestamp = date

        return embed

def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')
