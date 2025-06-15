import discord
from discord import app_commands
from discord.ext import commands

class Pong(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pong", description="Replies with Pong!")
    async def pong(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong from slash command!")

async def setup(bot):
    await bot.add_cog(Pong(bot))