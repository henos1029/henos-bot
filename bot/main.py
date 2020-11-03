import os
os.system('pip install --upgrade pip')
os.system('pip install youtube_dl')
os.system('pip install --upgrade youtube_dl')
os.system('pip install dblpy')
os.system('pip install henostools')
os.system('pip install hoster')
os.system('pip install discord.py[voice]')
os.system('pip install hcolours')
os.system('pip install python-dotenv')
os.system('pip install pyshortener')
os.system('clear')
from discord.ext import commands  #, tasks
import discord
import asyncio
import hoster
import tools
import random
from replit import db
import hcolours
import logging, traceback
from dotenv import load_dotenv

intents = discord.Intents.all()
loop = asyncio.get_event_loop()
status = "'hb: help'"
statushh = "henos's bots"
hb = commands.Bot(
    command_prefix=commands.when_mentioned_or('hb: ', 'hb:'),
    intents=intents,
    loop=loop,
    activity=discord.Activity(type=discord.ActivityType.watching, name=status))
hh = commands.Bot(
    command_prefix='h.h: ',
    intents=intents,
    loop=loop,
    activity=discord.Activity(
        type=discord.ActivityType.watching, name=statushh))
red = discord.Colour.red()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

load_dotenv()
hb_TOKEN = os.getenv('HBTOKEN')
hh_TOKEN = os.getenv('HHTOKEN')
"""
henos bot
"""

@hb.event
async def on_error(event, *args, **kwargs):
    print(f'Something went wrong!\nThe error happened in {event} event\nDetails: {args}\n{kwargs}')
    print('Traceback:', logging.warning(traceback.format_exc()))


@hb.event
async def on_ready():
    print(f'{hb.user} is online!')
    print(
        f'{hcolours.colour.red}Guild Count:{hcolours.reset} {len(hb.guilds)}')
    print(
        f'{hcolours.colour.red}Member Count:{hcolours.reset} {len(hb.users)}')
    items = [
            'Cookie', 'Chocolate', 'Coin', 'Rare Coin', 'Medal', 'Rare Medal',
            'Trophy', 'Rare Trophy', 'Ultra Collectable Thingy'
        ]
    for item in items:
        print(f'{item} = {db[item]}')
    print(f'Invite url: {discord.utils.oauth_url(hb.user.id, permissions= discord.Permissions(permissions=8))}')

# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc1NjMxMDYzMjc5MzUwNTgzMiIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA0MjYyNDEzfQ.LUFqnK-1981gkd4OXaGFaNhaEVM9fFZ0g628_bixAYo'
# dblpy = dbl.DBLClient(
#             hb,
#             token,
#             webhook_path='/dblwebhook',
#             webhook_auth='henos-bot',
#             webhook_port=5000,
#             autopost=True
# )

# @hb.event
# async def on_dbl_vote(data):
#     """An event that is called whenever someone votes for the bot on top.gg."""
#     print("Received an upvote:", "\n", data, sep="")

# @hb.event
# async def on_dbl_test(data):
#     print('test received')

# @hb.event
# async def on_guild_post():
#     print("Server count posted successfully")

@hb.event
async def on_guild_join(guild):
    channel = guild.system_channel
    embed = discord.Embed(
        title=f'Hello {guild.name}',
        description=
        f"I'm {hb.user} ({hb.user.mention})\nThanks for adding me to your server"
    )
    embed.set_footer(text='Use `hb: help` to get a list of my commands')
    await channel.send(embed=embed)


@hb.event
async def on_command_error(ctx, error):
    if not isinstance(error, commands.CommandOnCooldown) and not isinstance(
            error, commands.CommandNotFound):
        embed = discord.Embed(
            title='Oh no!',
            description=
            f'There was a error with the {ctx.command.name} command\n\nError: {error}',
            colour=red)
        await ctx.send(embed=embed)
        await ctx.send(f'Traceback: {traceback.format_exc()}')
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f'This command is on a cooldown. Please wait {round(error.retry_after)} seconds'
        )
    else:
        return


@hb.event
async def on_message(message):
    await tools.open_account(message.author.id)
    wallet, bank, xp, level = db[message.author.id].split(',')
    if not message.author.bot:
        xp_new = int(xp) + 1
        db[message.author.id] = f'{wallet},{bank},{xp_new},{level}'
        if xp_new >= 49:
            level_new = int(level) + 1
            db[message.author.id] = f'{wallet},{bank},0,{level_new}'
            await message.channel.send(
                f"Well done {message.author.mention}!! You are now level {level}"
            )
    await hb.process_commands(message)


@hb.event
async def on_command_completion(ctx):
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

    msg = await hb.wait_for('message', check=check)
    if msg:
        await tools.save(user=msg.author.id, amount=amount)
        await ctx.send(
            f'Congrats {msg.author.mention}!, you got {amount} dollars')
    else:
        await ctx.send('Too bad :(, nothing for you')


# welcome
@hb.event
async def on_member_join(member):
    blacklisted_guilds = [
        739811956638220298, 568902211980099605, 454409434676854786, 374071874222686211
    ]
    channel = member.guild.system_channel
    if member.guild.id not in blacklisted_guilds:
        if not member.bot:
            await member.send(
                f'Hi {member.name}, welcome to {member.guild.name}!, use `hb: help` to get a list of the commands'
            )
            await channel.send(
                f'Hi {member.name}, welcome to {member.guild.name}!, use `hb: help` to get a list of the commands'
            )


"""
h. helper
"""


@hh.event
async def on_ready():
    print(f'{hh.user} is online!')
    hh.load_extension('cogs.hhcog')


hbextentions = [
    'cogs.hbmusic',
    'cogs.hbeconomy',
    'cogs.hbfun',
    'cogs.hbrank',
    'cogs.hbmoderation',
    'cogs.hbutils'
    #'cogs.hbinfinity+'
    #'cogs.hbupvote'
]
for extension in hbextentions:
    hb.load_extension(extension)

hh.remove_command('help')
# hb.remove_command('help')

@hh.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send('You need to be the owner of the bot to use this command.')

@hh.command()
@commands.is_owner()
async def start(ctx, mode):
    if mode == 'bot' or mode == 'all':
        hbextentions = [
            'cogs.hbmusic', 'cogs.hbeconomy', 'cogs.hbfun', 'cogs.hbrank',
            'cogs.hbmoderation', 'cogs.hbutils', 'cogs.hbinfinity+'
        ]
        for extension in hbextentions:
            hb.load_extension(extension)
    else:
        hb.load_extension('cogs.hb' + mode)
    await ctx.send(f'{hb.user.mention} has started')


@hh.command()
@commands.is_owner()
async def restart(ctx, mode):
    if mode == 'bot' or mode == 'all':
        hbextentions = [
            'cogs.hbmusic', 'cogs.hbeconomy', 'cogs.hbfun', 'cogs.hbrank',
            'cogs.hbmoderation', 'cogs.hbutils', 'cogs.hbinfinity+'
        ]
        for extension in hbextentions:
            hb.reload_extension(extension)
    else:
        hb.reload_extension('cogs.hb' + mode)
    await ctx.send(f'{hb.user.mention} has restarted')


@hh.command()
@commands.is_owner()
async def stop(ctx, mode):
    if mode == 'bot' or mode == 'all':
        hbextentions = [
            'cogs.hbmusic', 'cogs.hbeconomy', 'cogs.hbfun', 'cogs.hbrank',
            'cogs.hbmoderation', 'cogs.hbutils', 'cogs.hbinfinity+'
        ]
        for extension in hbextentions:
            hb.load_extension(extension)
    else:
        hb.unload_extension('cogs.hb' + mode)
    await ctx.send(f'{hb.user.mention} has stopped')


hoster.start()
loop.create_task(hh.start(hh_TOKEN))
hb.run(hb_TOKEN)
