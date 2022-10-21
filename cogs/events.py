import discord
import imagehash
import os
import json
import numpy as np
from PIL import Image
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name}#{self.bot.user.discriminator} is ready!')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if not message.attachments:
            return
        
        if not message.guild:
            return
        
        hashes: list[imagehash.ImageHash] = []
        for attachment in message.attachments:
            await attachment.save(f'images/image_{message.id}.png')
            hashes.append(imagehash.average_hash(Image.open(f'images/image_{message.id}.png')))
            os.remove(f'images/image_{message.id}.png')
        
        with open('images.json', 'r') as f:
            forbidden_images = json.load(f)
        
        if str(message.guild.id) not in forbidden_images:
            return
                                
        for h, image in zip(hashes, forbidden_images[str(message.guild.id)][0].values()):
            if h - imagehash.ImageHash(np.asarray(image)) < 5:
                await message.delete()
                return


def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))
