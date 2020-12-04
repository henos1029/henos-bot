import os
os.system('pip install --upgrade pip')
os.system('pip install youtube_dl')
os.system('pip install henostools')
os.system('pip install hoster')
os.system('pip install python-dotenv')
os.system('pip install git+https://github.com/Rapptz/discord-ext-menus')
os.system('pip install enhanced-dpy[voice]')
os.system('pip install hcolours')
os.system('pip install jishaku')
os.system('pip install alexflipnote.py')
os.system('pip install aiosqlite')
os.system('clear')
import logging, traceback, discord, henostools, asyncio, hoster, tools, random, hcolours, time, datetime, aiosqlite
from dotenv import load_dotenv
from discord.ext import commands  #, tasks
import replit

runtime = datetime.datetime.now()

class henos_bot(commands.AutoShardedBot):
# class henos_bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_error(self, event, *args, **kwargs):
        print(f'Something went wrong!\nThe error happened in {event} event\nDetails: {args}\n{kwargs}')
        print('Traceback:', logging.warning(traceback.format_exc()))

    async def on_ready(self):
        print(f'{self.user} ({self.user.id}) is online!')
        startuptime = datetime.datetime.now()
        self.startuptime = startuptime - runtime
        print(f'Startup time is {self.startuptime.seconds} seconds')
        await henostools.sleep('1m')
        print(
            f'{hcolours.colour.red}Guild Count:{hcolours.reset} {len(self.guilds)}')
        print(
            f'{hcolours.colour.red}Member Count:{hcolours.reset} {len(self.users)}')
        items = [
                'Cookie', 'Chocolate', 'Coin', 'Rare Coin', 'Medal', 'Rare Medal',
                'Trophy', 'Rare Trophy', 'Ultra Collectable Thingy'
            ]
        for item in items:
            print(f'{item} = {replit.db[item]}')
        print(f'Invite url: {discord.utils.oauth_url(self.user.id, permissions= discord.Permissions(permissions=8))}')
        print(f'Owner: {self.get_user(self.owner_id)}')
        print(f'Shards: ({len(self.shards)})')
        self.db = await aiosqlite.connect('database.db')
        # db = self.db
        # cur = await db.execute('SELECT * FROM balance')
        # res = await cur.fetchall()
        # print(res)
        # cur = await db.execute('SELECT * FROM levels')
        # res = await cur.fetchall()
        # print(res)
        # await db.close()
        # db = await aiosqlite.connect('database.db')
        # await db.execute('CREATE TABLE IF NOT EXISTS balance (user INTEGER, wallet INTEGER, bank INTEGER)')
        # await db.commit()
        # await db.close()
        # db = await aiosqlite.connect('database.db')
        # await db.execute('CREATE TABLE IF NOT EXISTS levels (user INTEGER, xp INTEGER, level INTEGER)')
        # await db.commit()
        # await db.close()
        await henostools.sleep('99999999999999999999999999999h')
        print('wow, stronk bot')

    async def on_resume(self):
        print(f'{self.user} ({self.user.id}) has resumed')
    
    async def on_connect(self):
        print(f'{self.user} ({self.user.id}) has connected')
        self.uptime = datetime.datetime.utcnow()
    
    async def on_shard_connect(self, shard_id):
        print(f'{self.user}\'s {shard_id} has connected')
    
    async def on_disconnect(self):
        print(f'{self.user} ({self.user.id}) has disconnected')
        runtime = datetime.datetime.now()
    
    async def on_shard_disconnect(self, shard_id):
        print(f'{self.user}\'s {shard_id} has disconnected')
    
    async def on_shard_resume(self):
        print(f'{self.user} ({self.user.id}) has resumed')
    
    async def on_shard_ready(self, shard_id):
        print(f'{self.user}\'s {shard_id} is ready')

    async def on_guild_join(self, guild):
        try:
            channel = guild.system_channel
            embed = discord.Embed(
                title=f'Hello {guild.name}',
                description=
                f"I'm {self.user} ({self.user.mention})\nThanks for adding me to your server"
            )
            embed.set_footer(text='Use `hb: help` to get a list of my commands')
            await channel.send(embed=embed)
        except Exception:
            pass
        finally:
            me = self.get_user(self.owner_id)
            await me.send(f'Woo hoo!\nI just got added to {guild.name}!!\nIn case you need to contact the owner of the server, here is their name and id:\n{guild.owner} ({guild.owner.id})')
    
    async def on_guild_remove(self, guild):
        print(f'I just got removed from {guild.name} :)\nIf you want to contact the owner, here is their name and id:\n{guild.owner} ({guild.owner.id})')

    async def on_command_error(self, ctx, error):
        if not isinstance(error, commands.CommandOnCooldown) and not isinstance(
                error, commands.CommandNotFound) and not isinstance(error, commands.MissingRequiredArgument) and not isinstance(error, commands.CheckFailure):
            embed = discord.Embed(
                title='Oh no!',
                description=
                f'There was a error with the {ctx.command.name} command\n\nError: {error}')
            await ctx.send(embed=embed)
            await ctx.send(f'Traceback: {traceback.format_exc()}')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f'This command is on a cooldown. Please wait {round(error.retry_after)} seconds'
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'You are missing the required argument `{error.param.name}`. Please try again with it.')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(error)
        else:
            if not isinstance(error, commands.CommandNotFound):
                await ctx.send(error)

    async def on_message(self, message):
        if message.guild == None:
            if message.author != self.user:
                me = self.get_user(self.owner_id)
                await me.send(f'hey henos, I just got sent a message from {message.author.mention}! Here it is:\n{message.content}')
        else:
            try:
                try:
                    await tools.open_account(message.author.id)
                    db = await aiosqlite.connect('database.db')
                    cur = await db.execute('SELECT xp,level FROM levels WHERE user=?', (message.author.id,))
                    rows = await cur.fetchone()
                    xp = rows[0]
                    level = rows[1]
                    await db.close()
                except Exception as e:
                    await self.process_commands(message)
                    print(e)
                    return
                if not message.author.bot:
                    xp_new = int(xp) + 1
                    db = await aiosqlite.connect('database.db')
                    await db.execute('UPDATE levels SET xp=? WHERE user=?', (xp_new, message.author.id,))
                    await db.commit()
                    await db.close()
                    if xp_new >= 49:
                        level_new = int(level) + 1
                        db = await aiosqlite.connect('database.db')
                        await db.execute('UPDATE levels SET level=? WHERE user=?', (level_new, message.author.id))
                        await db.commit()
                        await db.close()
                        db = await aiosqlite.connect('database.db')
                        await db.execute('UPDATE levels SET xp=? WHERE user=?', (0, message.author.id))
                        await db.commit()
                        await db.close()
                        ignored = replit.db['Ignored']
                        if not message.guild is None:
                            if message.guild.id not in ignored:
                                msg = await message.channel.send(
                                    f"Well done {message.author.mention}!! You are now level {level_new}"
                                )
                                await henostools.sleep('10s')
                                try:
                                    await msg.delete()
                                except Exception:
                                    pass
            except Exception as e:
                print(e)
                pass
        await self.process_commands(message)

    async def on_command_completion(self, ctx):
        await tools.open_account(ctx.author.id)
        chance = random.randrange(0, 40)
        ttt = [
            'hi, im dumb', 'jkdvbekjcnejcbne', 'blah blah blah', 'blabity blab',
            'henos bot is THE BEST', 'kjdcijnr', 'kcnec ekcjeovcie ecojecioe',
            'keceivcjhrnvi', '129048907393', '1234567890', '0987654321',
            '(*%&^%%^*&*%)'
        ]
        tttc = random.choice(ttt)
        if chance == 1:
            await ctx.send(f'Common Event time!!\npls type `{tttc}`')
            amount = random.randrange(10, 100)
        elif chance == 10:
            await ctx.send(f'Uncommon Event time!!\npls type `{tttc}`')
            amount = random.randrange(50, 200)
        elif chance == 20:
            await ctx.send(f'Rare Event time!!\npls type `{tttc}`')
            amount = random.randrange(100, 500)
        elif chance == 30:
            await ctx.send(f'Legendary Event time!!\npls type `{tttc}`')
            amount = random.randrange(500, 2000)
        elif chance == 39:
            await ctx.send(f'Mythic Event time!!\npls type `{tttc}`')
            amount = random.randrange(1000, 5000)
        else:
            return

        def check(msg):
            return msg.content == tttc

        msg = await self.wait_for('message', check=check)
        if msg:
            await tools.save(user=msg.author.id, amount=amount)
            await ctx.send(
                f'Congrats {msg.author.mention}!, you got {amount} dollars')
        else:
            await ctx.send('Too bad :(, nothing for you')

    async def on_member_join(self, member):
        blacklisted_guilds = replit.db['Ignored']
        channel = member.guild.system_channel
        if member.guild.id not in blacklisted_guilds:
            if not member.bot:
                try:
                    await channel.send(
                        f'Hi {member.name}, welcome to {member.guild.name}!, use `hb: help` to get a list of the commands'
                    )
                except Exception:
                    pass

    async def on_member_remove(self, member):
        blacklisted_guilds = replit.db['Ignored']
        channel = member.guild.system_channel
        if member.guild.id not in blacklisted_guilds:
            if not member.bot:
                try:
                    await channel.send(
                        f'Awww, {member} just left {member.guild.name} :('
                    )
                except Exception:
                    pass

intents = discord.Intents.all()
loop = asyncio.get_event_loop()
status = "'hb: help'"
statushh = "henos's bots"
hb = henos_bot(
    command_prefix=commands.when_mentioned_or('hb: ', 'hb:'),
    intents=intents,
    loop=loop,
    activity=discord.Activity(type=discord.ActivityType.watching, name=status))
class h_helper(commands.Bot):
    async def on_ready(self):
        print(f'{self.user} ({self.user.id}) is online!')
hh = h_helper(
    command_prefix='h.h: ',
    intents=intents,
    loop=loop,
    activity=discord.Activity(type=discord.ActivityType.watching, name=statushh))
hb.set_embed_color(discord.Colour.red())
hb.owner_id = 717633235789807657

load_dotenv()
hb_TOKEN = os.getenv('HBTOKEN')
hh_TOKEN = os.getenv('HHTOKEN')

hb.remove_command('help')
hbextentions = [
    'cogs.hbmusic',
    'cogs.hbeconomy',
    'cogs.hbfun',
    'cogs.hbrank',
    'cogs.hbmoderation',
    'cogs.hbutils',
    'cogs.hbhelp',
    'jishaku',
    'cogs.hbtsos',
    'cogs.hbchristmas',
    'cogs.hbimage'
]
for extension in hbextentions:
    hb.load_extension(extension)
    print(f'{extension} loaded succesfuly')

time.sleep(5)
os.system('clear')

hh.remove_command('help')
hh.load_extension('cogs.hhcog')
hh.load_extension('jishaku')

@hh.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send('You need to be the owner of the bot to use this command.')
    else:
        await ctx.send(error)

@hb.command()
@commands.is_owner()
async def test(ctx):
  await ctx.reply('hi')

hoster.start()
loop.create_task(hh.start(hh_TOKEN))
hb.run(hb_TOKEN)
