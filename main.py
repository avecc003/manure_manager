import discord
import os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv("bot_token")

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    async def setup_hook(self):
        # Register slash command
        self.tree.add_command(pong)
        await self.tree.sync()  # Sync with Discord

@commands.command()
async def legacy_ping(ctx):
    await ctx.send("Pong from legacy command!")

@discord.app_commands.command(name="pong", description="Replies with Pong!")
async def pong(interaction: discord.Interaction):
    await interaction.response.send_message("Pong from slash command!")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

bot.run(BOT_TOKEN)
