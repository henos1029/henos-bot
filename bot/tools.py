import json
import discord
from replit import db

red = discord.Colour.red()

async def open_account(user: str):
    if user not in db.keys():
        db[user] = '500,0,0,0'
        return True
    else:
        return False

async def save(user: str, amount: int):
    wallet, bank, xp, level = db[user].split(',')
    db[user] = f'{int(wallet) +  amount},{bank},{xp},{level}'

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
    Medal = 10000
    RareMedal = 50000
    Trophy = 100000
    RareTrophy = 500000
    UltraCollectableThingy = 1000000

cool_people = [717633235789807657, 766555259220787220, 727350727713882183, "if rish joins bpoc: 'rish's id'"]
