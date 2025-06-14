import discord
import os
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv("bot_token")

# Intents are required to access certain gateway events
intents = discord.Intents.default()
intents.message_content = True  # Enable access to message content

# Define bot prefix and intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f"Bot is online! Logged in as {bot.user} (ID: {bot.user.id})")

# Command: Ping
@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")

# Command: Echo
@app_commands.command(name="echo", description="Echo a message")
async def echo(ctx, *, message: str):
    await ctx.send(message)

if __name__ == "__main__":
    if BOT_TOKEN:
        bot.run(BOT_TOKEN)
    else:
        print("Error: DISCORD_BOT_TOKEN not set in environment variables.")
