# Load a Library for the bot
from typing import Literal, Union, NamedTuple
from enum import Enum
import asyncio

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

@client.tree.command()
@app_commands.describe(first='The first number to add', second='The second number to add')
async def add(
    interaction: discord.Interaction,
    first: app_commands.Range[int, 0, 100],
    second: app_commands.Range[int, 0, None],
):
    """Adds two numbers together"""
    await interaction.response.send_message(f'{first} + {second} = {first + second}', ephemeral=True)

@client.tree.command(name='channel-info')
@app_commands.describe(channel='The channel to get info of')
async def channel_info(interaction: discord.Interaction, channel: Union[discord.VoiceChannel, discord.TextChannel]):
    """Shows basic channel info for a text or voice channel."""

    embed = discord.Embed(title='Channel Info')
    embed.add_field(name='Name', value=channel.name, inline=True)
    embed.add_field(name='ID', value=channel.id, inline=True)
    embed.add_field(
        name='Type',
        value='Voice' if isinstance(channel, discord.VoiceChannel) else 'Text',
        inline=True,
    )

    embed.set_footer(text='Created').timestamp = channel.created_at
    await interaction.response.send_message(embed=embed)

@client.tree.command()
@app_commands.describe(action='The action to do in the shop', item='The target item')
async def shop(interaction: discord.Interaction, action: Literal['Buy', 'Sell'], item: str):
    """Interact with the shop"""
    await interaction.response.send_message(f'Action: {action}\nItem: {item}')

class Fruits(Enum):
    apple = 0
    banana = 1
    cherry = 2
    dragonfruit = 3

@client.tree.command()
@app_commands.describe(fruit='The fruit to choose')
async def fruit(interaction: discord.Interaction, fruit: Fruits):
    """Choose a fruit!"""
    await interaction.response.send_message(repr(fruit))

class Point(NamedTuple):
    x: int
    y: int

class PointTransformer(app_commands.Transformer):
    async def transform(self, interaction: discord.Interaction, value: str) -> Point:
        (x, _, y) = value.partition(',')
        return Point(x=int(x.strip()), y=int(y.strip()))

client.run(os.environ['TOKEN'])