import discord
import datetime
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='help', description='Helps with all commands!')
    async def help(self, ctx: commands.Context, command: str | None = None):
        prefix = 'i!'

        if command is None:
            # Create embed
            embed = discord.Embed(
                title='Help Page',
                description=f'Shows the list of all commands\nUse `{prefix}help <command>` to get more information about a command',
                colour=discord.Colour.blurple(),
                timestamp=datetime.datetime.now()
            ).set_footer(text='Help Page', icon_url=self.bot.user.avatar.url)

            for cog in sorted(self.bot.cogs):
                if cog in ['Owner', 'Events']:
                    continue

                commands_str = ''.join(f'`{command.name}` ' for command in self.bot.cogs[cog].get_commands())
                embed.add_field(name=cog, value=commands_str[:-1], inline=False)

        else:
            cmd = self.bot.get_command(command)

            if cmd is None:
                await ctx.reply(f'Command {command} not does not exist!')

            # Create embed
            embed = discord.Embed(
                title=f'Help - {cmd}',
                description=cmd.description,
                colour=discord.Colour.blurple(),
                timestamp=datetime.datetime.now()
            )
            embed.set_footer(text=f'Help for {cmd}', icon_url=self.bot.user.avatar.url)

            param_str = ''.join(f'`{param}` ' for param in cmd.clean_params)[:-1]
            embed.add_field(name='Usage', value=f'{prefix}{cmd.name} {param_str or "`None`"}')

        await ctx.reply(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))
