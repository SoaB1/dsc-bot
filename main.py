# Load a Library for the bot
from asyncio.log import logger
import os, dotenv, discord, asyncio
import logging
import logging.handlers
from discord.ext import commands
from dotenv import load_dotenv

# import formatter
load_dotenv()

COGS = [
    'cog.commands'
]

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

class MyBot(commands.Bot):
    def __init__(self, prefix: str, intents: discord.Intents):
        super().__init__(command_prefix=prefix, intents=intents)
    
    async def on_ready(self):
        print(f'Logged in as {self.user}#{self.user.id}')

async def main():
    
    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    
    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        mode='w',
        maxBytes=100000,
        backupCount=5
    )
    date_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', datefmt=date_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    bot = MyBot(intents=discord.Intents.all(), prefix='/')
    for cog in COGS:
        await bot.load_extension(cog)
        
    await bot.start(os.environ['TOKEN'])

if __name__ == '__main__':
    asyncio.run(main())