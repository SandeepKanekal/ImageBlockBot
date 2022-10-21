import discord
import os
from discord.ext import commands
from dotenv import load_dotenv


def main():
    load_dotenv()

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix=commands.when_mentioned_or('i!'), help_command=None, intents=intents)

    for file in os.listdir('./cogs'):
        if file.endswith(".py"):
            bot.load_extension(f'cogs.{file[:-3]}')

    bot.run(os.getenv('image_bot_token'))


if __name__ == "__main__":
    main()
