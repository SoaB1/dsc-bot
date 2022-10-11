# Load a Library for the bot
from typing import Literal, Union, NamedTuple
from enum import Enum

import discord
from discord import app_commands
import os
import dotenv
from dotenv import load_dotenv

# Load a Library for local files
from src import spreadsheet

load_dotenv()
MY_GUILD = discord.Object(id=983017319766827038)

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

client = MyClient()

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.tree.command()
async def ticket(interaction: discord.Interaction):
    ticketNum = await spreadsheet.getTicketNumber()
    embed = discord.Embed(title='New Ticket', description='Please fill out the following form, information to create a new ticket.', color=0x00ff00)
    embed.add_field(name='Ticket Number', value=ticketNum, inline=False)
    embed.add_field(name='URL', value=os.environ['FORM_URL'])
    await interaction.response.send_message(embed=embed)

client.run(os.environ['TOKEN'])