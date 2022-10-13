import discord
import os
from discord.ext import commands
from discord import app_commands
from src import spreadsheet

class ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name='ticket', description='Create a new ticket')
    async def ticket(self, interaction: discord.Interaction):
        ticketNum = await spreadsheet.getTicketNumber()
        embed = discord.Embed(title='New Ticket', description='Please fill out the following form, information to create a new ticket.', color=0x00ff00)
        embed.add_field(name='Ticket Number', value=ticketNum, inline=False)
        embed.add_field(name='URL', value=os.environ['FORM_URL'])
        await interaction.response.send_message(embed=embed)
    
async def setup(bot: commands.Bot):
    await bot.add_cog(ticket(bot))