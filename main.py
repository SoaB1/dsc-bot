# Load a Library for the bot
from cmath import log
import os, dotenv, discord, asyncio, logging
from discord.ext import commands
from dotenv import load_dotenv
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
    bot = MyBot(intents=discord.Intents.all(), prefix='/')
    for cog in COGS:
        await bot.load_extension(cog)
        
    # await bot.start(os.environ['TOKEN'])
    await bot.start(os.environ['TOKEN'], log_handler=handler)

if __name__ == '__main__':
    asyncio.run(main())