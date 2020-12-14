from discord.ext import commands
import discord
import tools

red = discord.Colour.red()

class TSOS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
      if member.guild.id == 777751872941457428:
        roles = [777769796556816434, 777763434544627734, 777763429674123267, 777762589622927401, 777762729782935552]
        for role in roles:
          role = member.guild.get_role(role)
          await member.add_roles(role)
      else:
        return
    
    @commands.Cog.listener()
    async def on_message(self, message):
      if message.guild is not None:
        if message.guild.id == 777863104188907520:
          guild = self.bot.get_guild(777751872941457428)
          channel = guild.get_channel(777776544365412362)
          await channel.send(message.content)
        else:
          return
      else:
        return

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 778195861804679180:
            roles = self.bot.get_guild(payload.guild_id)
            member = roles.get_member(payload.user_id)
            roles = roles.roles
            role = discord.utils.get(roles, name=tools.colours[payload.emoji.name])
            await member.add_roles(role)
        elif payload.message_id == 778197781050818570:
            roles = self.bot.get_guild(payload.guild_id)
            member = roles.get_member(payload.user_id)
            roles = roles.roles
            role = discord.utils.get(roles, name=tools.roles[payload.emoji.name])
            await member.add_roles(role)
        else:
            return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 778195861804679180:
            roles = self.bot.get_guild(payload.guild_id)
            member = roles.get_member(payload.user_id)
            roles = roles.roles
            role = discord.utils.get(roles, name=tools.colours[payload.emoji.name])
            await member.remove_roles(role)
        elif payload.message_id == 778197781050818570:
            roles = self.bot.get_guild(payload.guild_id)
            member = roles.get_member(payload.user_id)
            roles = roles.roles
            role = discord.utils.get(roles, name=tools.roles[payload.emoji.name])
            await member.remove_roles(role)
        else:
            return
    
    @commands.group()
    async def tsos(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                'Invalid command.\nExample: `hb: tsos <command>`'
            )

    @tsos.command()
    async def verify(self, ctx):
      await ctx.message.delete()
      await ctx.send(f'{ctx.author.mention}, please check you dms.', delete_after=30)
      await ctx.author.send(f'Verification Process has started...\n\nPlease enter your username and discriminator to verify your account.\ne.g.: `henos bot#2743`')
      def verifycheck(msg):
        return msg.content == str(ctx.author)
      msg = await self.bot.wait_for('message', check=verifycheck)
      if msg:
        await ctx.author.send('You have successfuly verified your account, head back to `The Server OF Servers` to start chatting')
        await ctx.author.add_roles(ctx.guild.get_role(777752087747493908))
      else:
        await ctx.author.send('Incorrect response, please run the command again')

def setup(bot):
    bot.add_cog(TSOS(bot))
