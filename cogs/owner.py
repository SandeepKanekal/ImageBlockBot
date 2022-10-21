import discord
from discord.ext import commands


class Owner(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name='reload')
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, cog: str):
        self.bot.reload_extension(f'cogs.{cog}')
        await ctx.reply("Reloaded!")
    
    @reload.error
    async def reload_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.reply(str(error))


def setup(bot: commands.Bot):
    bot.add_cog(Owner(bot))
