import discord
import os
from discord.ext import commands
from src import spreadsheet

class BasicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
    
    @commands.command()
    # async def test(self,ctx):
        # await ctx.send("test!")
    async def ticket(self, ctx):
        ticketNum = await spreadsheet.getTicketNumber()
        embed = discord.Embed(title='New Ticket', description='Please fill out the following form, information to create a new ticket.', color=0x00ff00)
        embed.add_field(name='Ticket Number', value=ticketNum, inline=False)
        embed.add_field(name='URL', value=os.environ['FORM_URL'])
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(BasicCog(bot))