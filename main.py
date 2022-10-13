# Load a Library for the bot
import asyncio
import discord
from discord.ext import commands
import asyncio
import os
import dotenv
from dotenv import load_dotenv
load_dotenv()

COGS = [
    'cog.commands'
]

class MyBot(commands.Bot):
    def __init__(self, prefix: str, intents: discord.Intents):
        super().__init__(command_prefix=prefix, intents=intents)
    
    async def on_ready(self):
        print(f'Logged in as {self.user}#{self.user.id}')

async def main():
    bot = MyBot(intents=discord.Intents.all(), prefix='/')
    for cog in COGS:
        await bot.load_extension(cog)
        
    await bot.start(os.environ['TOKEN'])

if __name__ == '__main__':
    asyncio.run(main())