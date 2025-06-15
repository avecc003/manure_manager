import discord
from discord import app_commands
from discord.ext import commands
from datetime import timedelta

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="poll", description="Replies with a Poll!")
    async def poll(self, interaction: discord.Interaction, text1: str, text2: str, text3: str=None):
        # maximum of 10 answers in a poll.
        poll = discord.Poll(question="Test", duration=timedelta(hours=1.0))
        poll.add_answer(text=text1)
        poll.add_answer(text=text2)
        if text3:
            poll.add_answer(text="text3")
        await interaction.response.send_message(poll=poll)

async def setup(bot):
    await bot.add_cog(Poll(bot))