from discord.ext import commands, menus
import discord
import tools

red = discord.Colour.red()

class HelpMenu(menus.Menu):
    async def update(self, payload):
        if self._can_remove_reactions:
            if payload.event_type == 'REACTION_ADD':
                await self.bot.http.remove_reaction(
                    payload.channel_id, payload.message_id,
                    discord.Message._emoji_reaction(payload.emoji), payload.member.id
                )
            elif payload.event_type == 'REACTION_REMOVE':
                return
        await super().update(payload)

    async def send_initial_message(self, ctx, channel):
        global counter
        counter = 1
        return await channel.send(embed=tools.helpdict[counter].set_footer(text=f'Page {counter}/7'))

    @menus.button('\U000025c0\U0000fe0f')
    async def on_back_page(self, payload):
        global counter
        counter -= 1
        if counter <= 0:
            counter = 7
        await self.message.edit(embed=tools.helpdict[counter].set_footer(text=f'Page {counter}/7'))
        user = await self.bot.get_guild(payload.guild_id).fetch_member(payload.user_id)
        try:
            await self.message.remove_reaction(payload.emoji, user)
        except:
            pass

    @menus.button('\U000025b6\U0000fe0f')
    async def on_next_page(self, payload):
        global counter
        counter += 1
        if counter > 7:
            counter = 1
        await self.message.edit(embed=tools.helpdict[counter].set_footer(text=f'Page {counter}/7'))
        user = await self.bot.get_guild(payload.guild_id).fetch_member(payload.user_id)
        try:
            await self.message.remove_reaction(payload.emoji, user)
        except:
            pass


    @menus.button('\U000023f9\U0000fe0f')
    async def on_stop(self, payload):
        self.stop()
        user = await self.bot.get_guild(payload.guild_id).fetch_member(payload.user_id)
        try:
            await self.message.remove_reaction(payload.emoji, user)
        except:
            pass

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        menu = HelpMenu()
        await menu.start(ctx)

def setup(bot):
    bot.add_cog(Help(bot))
