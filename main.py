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
        await self.load_extension("cogs.pong")
        await self.load_extension("cogs.poll")
        await self.tree.sync()  # Sync with Discord

bot = MyBot()

# References command tree directly.
@bot.tree.command(name="reload", description="reload cog")
async def reload(interaction: discord.Interaction):
    failed = []
    # list all directories in ./cogs, and attempt to reload. failed cog reloads are appended to 'failed' list.
    for filename in os.listdir("cogs"): 
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}" 
            try:
                await bot.reload_extension(cog_name) 
            except Exception as e:
                failed.append(f"{cog_name}: {e}")

    # output all cogs that fail to reload, and print exception. else, print "Reloaded all Cogs!" 
    if len(failed) >= 1:
        failed_response = "The following Cogs failed to reload:\n"
        for failed_ext in failed:
            failed_response += failed_ext + '\n'
        await interaction.response.send_message(failed_response)
    else:
        await interaction.response.send_message("Reloaded all Cogs!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

bot.run(BOT_TOKEN)
