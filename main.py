import discord
import os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv("bot_token")


class MyClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.add_command(pong)  # Register the slash command

bot = MyClient()

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')
    await bot.tree.sync()  # Register commands with Discord

@app_commands.command(name="pong", description="Replies with Pong!")
async def pong(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

bot.run(BOT_TOKEN)