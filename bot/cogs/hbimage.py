import discord
from discord.ext import commands
import alexflipnote
import random
import sr_api
import os

class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afapi = alexflipnote.Client(os.getenv('AF_TOKEN'), loop=self.bot.loop)
        self.srapi = sr_api.Client()
    
    @commands.command(name='filter')
    async def filterafapi(self, ctx, filter, user: discord.Member = None):
        if user is None:
            user = ctx.author
        embed = discord.Embed(
          title=f'{filter}!!'
        )
        img = await self.afapi.filter(filter, user.avatar_url)
        file = discord.File(await img.read(), f"{filter}.png")
        embed.set_image(url=f'attachment://{filter}.png')
        await ctx.send(embed=embed, file=file)
    
    @commands.command()
    async def getimg(self, ctx, animal):
        img = await self.srapi.get_image(animal)
        embed = discord.Embed(
          title=f'{animal}!!'
        )
        print(img.url)
        file = discord.File(await img.read(), f"{animal}.png")
        embed.set_image(url=f'attachment://{animal}.png')
        await ctx.send(embed=embed, file=file)
    
    @commands.command()
    async def trash(self, ctx, user : discord.Member):
        embed = discord.Embed()
        img = await self.afapi.trash(ctx.author.avatar_url, user.avatar_url)
        file = discord.File(await img.read(), f"trash.png")
        embed.set_image(url=f'attachment://trash.png')
        await ctx.send(embed=embed, file=file)
    
    @commands.command()
    async def ship(self, ctx, user: discord.Member):
        embed = discord.Embed(
          title=f'Ship!!',
          description=f'{random.randrange(1,100)}% compatible!!'
        )
        embed.set_footer(text=f'{ctx.author.name} <3 {user.name}')
        img = await self.afapi.ship(ctx.author.avatar_url, user.avatar_url)
        file = discord.File(await img.read(), f"ship.png")
        embed.set_image(url=f'attachment://ship.png')
        await ctx.send(embed=embed, file=file)
    
    @commands.command()
    async def salty(self, ctx, user : discord.Member):
        embed = discord.Embed()
        img = await self.afapi.salty(user.avatar_url)
        file = discord.File(await img.read(), f"salty.png")
        embed.set_image(url=f'attachment://salty.png')
        await ctx.send(embed=embed, file=file)
    
    @commands.command()
    async def gradient(self, ctx, colour: str):
        embed = discord.Embed()
        img = await self.afapi.colour_image_gradient(colour=colour)
        file = discord.File(await img.read(), f"gradient.png")
        embed.set_image(url=f'attachment://gradient.png')
        await ctx.send(embed=embed, file=file)
    
    @commands.command()
    async def amiajoke(self, ctx, user : discord.Member = None):
        if user is None:
            user = ctx.author
        embed = discord.Embed()
        img = await self.afapi.amiajoke(user.avatar_url)
        file = discord.File(await img.read(), f"amiajoke.png")
        embed.set_image(url=f'attachment://amiajoke.png')
        await ctx.send(embed=embed, file=file)
    
    @commands.command()
    async def calling(self, ctx, *, text : str):
        embed = discord.Embed()
        img = await self.afapi.calling(text)
        file = discord.File(await img.read(), f"calling.png")
        embed.set_image(url=f'attachment://calling.png')
        await ctx.send(embed=embed, file=file)

def setup(bot):
  bot.add_cog(Image(bot))
