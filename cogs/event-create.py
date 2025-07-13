import discord, os, json, aiohttp
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

import re
from datetime import datetime, timedelta
import pytz

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
BOT_TOKEN = os.getenv("bot_token")

class EventCreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_api_url = 'https://discord.com/api/v10'
        self.auth_headers = {
            'Authorization': f'Bot {BOT_TOKEN}',
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
    async def eventCreate(self, interaction: discord.Interaction, name: str, start_time: str, end_time: str, location: str, description: str=None):
        # Stretch Goal: Add Google Image Search for location and add image to event.
        def parse_datetime(time_str):
            # Normalize string
            time_str = time_str.strip().lower().replace('.', '')

            # Regex patterns: MM/DD/YY HH:MM(am/pm) and MM/DD/YY HH(am/pm)
            date_pattern = r'(\d{1,2})/(\d{1,2})/(\d{2,4})'
            time_pattern = r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?'

            match = re.match(f'^{date_pattern}\\s+{time_pattern}$', time_str)
            if match is None:
                raise ValueError("Invalid date/time format. Please use MM/DD/YY HH(am/pm) or MM/DD/YY HH:MM(am/pm)")

            month, day, year, hour, minute, am_pm = match.groups()
            if am_pm is None:
                raise ValueError("AM/PM is required for time parsing.")
            
            # Use the first two digits of today's year as the century, and make it more future resistant
            # #allmydiscordfans #iloveyou
            current_year = datetime.now().year
            century = int(str(current_year)[:2])
            year = int(year)
            if year < 100:
                year += century * 100
            month = int(month)
            day = int(day)
            hour = int(hour)
            minute = int(minute) if minute else 0

            if am_pm:
                if am_pm == 'pm' and hour != 12:
                    hour += 12
                elif am_pm == 'am' and hour == 12:
                    hour = 0

            try:
                eastern = pytz.timezone('US/Eastern')
                dt_obj = eastern.localize(datetime(year, month, day, hour, minute))
            except Exception as e:
                raise ValueError(f"Could not parse datetime: {e}")

            # Discord expects ISO8601 format
            return dt_obj.isoformat(sep=' ')

        # Parse start and end times
        try:
            start_time = parse_datetime(start_time)
        except Exception as e:
            await interaction.response.send_message(f"Error parsing start time: {e}", ephemeral=True)
            return

        if end_time:
            try:
                end_time = parse_datetime(end_time)
            except Exception as e:
                await interaction.response.send_message(f"Error parsing end time: {e}", ephemeral=True)
                return

        # Format event creation url, and json payload
        event_create_url = f'{self.base_api_url}/guilds/{interaction.guild.id}/scheduled-events'
        event_data = json.dumps({
            'name': name,
            'privacy_level': 2,
            'scheduled_start_time': start_time,
            'scheduled_end_time': end_time,
            'description': description,
            'entity_metadata': {'location': location},
            'entity_type': 3
        })

        print(event_data)

        # Send HTTPS POST Request to Discord API with json payload embedded
        async with aiohttp.ClientSession(headers=self.auth_headers) as session:
            try:
                async with session.post(event_create_url, data=event_data) as response:
                    response.raise_for_status()
                    assert response.status == 200
            except Exception as e:
                print(f'EXCEPTION: {e}')
            finally:
                await session.close()
        
        await interaction.response.send_message(f"Event {name} created!")

async def setup(bot):
    await bot.add_cog(EventCreate(bot))