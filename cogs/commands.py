import discord
import contextlib
import imagehash
import requests
import os
import datetime
import json
from PIL import Image, UnidentifiedImageError
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='add', description='Add an image to be blocked.\nThough the argument is a URL, ONLY IMAGES SENT AS ATTACHMENTS ARE BLOCKED!')
    @commands.has_permissions(manage_messages=True)
    async def add_image(self, ctx: commands.Context, url: str):
        async with ctx.typing():
            with open(f'images/image_{ctx.message.id}.png', 'wb') as f:
                f.write(requests.get(url).content)

            image_hash = imagehash.average_hash(Image.open(f'images/image_{ctx.message.id}.png')).hash.tolist()

            os.remove(f'images/image_{ctx.message.id}.png')

            with open('images.json', 'r') as f:
                data = json.load(f)
            
            with contextlib.suppress(KeyError):
                if url in data[str(ctx.guild.id)][0]:
                    await ctx.reply('This image has already been blocked!')
                    return

            try:
                data[str(ctx.guild.id)][0][url] = image_hash
            except (KeyError, IndexError):
                data[str(ctx.guild.id)] = [{url: image_hash}]

            with open("images.json", "w") as f:
                json.dump(data, f, indent=3)
            
            await ctx.reply('Image added!')
    
    @add_image.error
    async def add_image_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, requests.exceptions.RequestException):
            await ctx.reply('Invalid URL Provided')
        
        elif isinstance(error, UnidentifiedImageError):
            await ctx.reply("Invalid URL Provided")
            os.remove(f'images/image_{ctx.message.id}.png')
        
        else:
            await ctx.reply(str(error))
    
    @commands.command(name='remove', description='Remove a blocked image!')
    @commands.has_permissions(manage_messages=True)
    async def remove_image(self, ctx: commands.Context, url: str):
        async with ctx.typing():
            with open('images.json', 'r') as f:
                data = json.load(f)
            
            with contextlib.suppress(KeyError):
                if url not in data[str(ctx.guild.id)][0]:
                    await ctx.reply('This image is not blocked!')
                    return
            
            del data[str(ctx.guild.id)][0][url]

            with open("images.json", "w") as f:
                json.dump(data, f, indent=3)
            
            await ctx.reply('Image removed!')
    
    @remove_image.error
    async def remove_image_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, requests.exceptions.RequestException):
            await ctx.reply('Invalid URL Provided')
        
        elif isinstance(error, UnidentifiedImageError):
            await ctx.reply("Invalid URL Provided")
            os.remove(f'images/image_{ctx.message.id}.png')
        
        else:
            await ctx.reply(str(error))

    @commands.command(name='list', description='List all blocked images!')
    async def list_images(self, ctx: commands.Context):
        with open('images.json', 'r') as f:
            urls = json.load(f)[str(ctx.guild.id)][0]

        embed = discord.Embed(
            title='Blocked Images!',
            description='\n'.join(f'{idx}. {url}' for idx, url in enumerate(urls)),
            colour=discord.Colour.blurple(),
            timestamp=datetime.datetime.now()
        )

        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url or discord.Embed.Empty)
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.display_avatar.url)

        await ctx.reply(embed=embed)

    @list_images.error
    async def list_images_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.reply(str(error))


def setup(bot: commands.Bot):
    bot.add_cog(Commands(bot))
