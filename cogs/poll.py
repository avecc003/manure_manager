import discord
import datetime
from discord import app_commands
from discord.ext import commands
from datetime import timedelta

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.polls = []

    @app_commands.command(name="poll", description="Replies with a Poll!")
    async def poll(self, interaction: discord.Interaction, text1: str, text2: str, text3: str=None):
        # maximum of 10 answers in a poll.
        poll = discord.Poll(question="Test", duration=timedelta(hours=1.0))
        poll.add_answer(text=text1)
        poll.add_answer(text=text2)
        if text3:
            poll.add_answer(text="text3")
        await interaction.response.send_message(poll=poll)
        
    @app_commands.command(name="poll_default", description="Replies with a Poll!")
    async def poll_default(self, interaction: discord.Interaction):
        curr_date = datetime.datetime.now()
        hours_left_in_day = 24 - curr_date.hour
        today = datetime.datetime(curr_date.year, curr_date.month, curr_date.day + 1)
        next_7_days = [today + timedelta(days=i) for i in range(7)]
        
        poll = discord.Poll(question="weekly poll", duration=timedelta(hours=hours_left_in_day), multiple=True )
        for day in next_7_days:
            poll.add_answer(text=day.strftime('%d/%m/%Y'))
        message = await interaction.response.send_message(poll=poll)
        self.polls.append(message)
        
    @app_commands.command(name="poll_end", description="Ends the current poll")
    async def end_last_poll(self, interaction: discord.Interaction):
        try:
            poll = self.polls.pop()        
            await interaction.response.send_message(f"Poll ended with {poll.results[0].emoji} as the result.")
            await poll.end()
        except:  
            await interaction.response.send_message("No poll to end.")
        
    # @commands.Cog.listener()
    # async def on_poll_end(self, poll, user) -> None:
    #     await poll.message.edit(content=f"Poll ended with {poll.results[0].emoji} as the result.")
    

async def setup(bot):
    await bot.add_cog(Poll(bot))