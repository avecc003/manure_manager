import discord, os, json, aiohttp
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

class EventCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_api_url = 'https://discord.com/api/v10'
        self.auth_headers = {
            'Authorization': f'Bot {load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))}',
            'User-Agent': 'DiscordBot (https://github.com/avecc003/manure_manager) Python/3.13.3 aiohttp/3.12.13',
            'Content-Type': 'application/json'
        }

    @app_commands.command(name="event-create", description="Create event with mentions for easy planning!")
    @app_commands.describe(
        name="Title",
        start_time="Start time in MM/DD/YY",
        end_time="End time in MM/DD/YY",
        location="Optional location for external event",
        description="Description"
        )
    async def eventCreate(self, interaction: discord.Interaction, name: str, start_time: str, end_time: str, location: str=None, description: str=None):
        #privacy_level = 2, only for this guild
        #location is supposed to be a dict in this format: location = {'location': f'{location}'}
        #channel_id references the voice channel id, which can be referenced in slash command via #!Speakathalon in discord text.
        #guild_id can be placed into the .env
        await interaction.response.send_message("Event created!")

async def setup(bot):
    await bot.add_cog(EventCreate(bot))