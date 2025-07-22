import discord, datetime
from discord import app_commands
from discord.ext import commands
from datetime import timedelta, datetime
from db import *

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="poll", description="Replies with a Poll, enter dates in MM/DD/YY!")
    @app_commands.describe(
        start = "List start date in MM/DD/YY",
        end = "List end date in MM/DD/YY",
        exclude = "List excluded dates in 'MM/DD/YY, ...' format",
        multiple = "Default multiple choice.",
        duration = "Default 1 hour."
    )
    async def poll(self, interaction: discord.Interaction, title: str, start: str, end: str, exclude: str=None, multiple: bool=True, duration: float=1.0):
        # Check if start and end dates are parsable before starting
        try: start_date = datetime.strptime(start, "%m/%d/%y")
        except ValueError: await interaction.response.send_message(f"Cannot parse start date ({start})."); return
        try: end_date = datetime.strptime(end, "%m/%d/%y")
        except ValueError: await interaction.response.send_message(f"Cannot parse end date ({end})."); return

        # Check if start date begins after end date
        if start_date > end_date:
            await interaction.response.send_message(f"Start date ({start}) is greater than end date ({end}).")
            return

        poll = discord.Poll(question=title, duration=timedelta(hours=duration), multiple=multiple)
        
        delta = end_date - start_date + timedelta(days=1) # delta used to create all date time objects between start and end dates
        check_date_length = delta # check_date_length used for error checking

        excluded_list = None
        if exclude:
            excluded_list = exclude.split(sep=",")

            # Clear whitespace in excluded dates
            try: stripped_list = [datetime.strptime(s.strip(), "%m/%d/%y") for s in excluded_list]
            except ValueError: await interaction.response.send_message(f"Cannot parse exclusion dates ({excluded_list})."); return

            # Create list of valid dates, used for calculating if total valid dates is within the poll's maximum of 10 answers.
            valid_dates = [date for date in stripped_list if (date > start_date and date < end_date)]
            check_date_length -= timedelta(days=len(valid_dates))

        if check_date_length.days > 7:
            await interaction.response.send_message(f"Total amount of dates ({check_date_length.days}) exceeds the maximum (7).")
            return

        for i in range(delta.days):
            list_date = start_date + timedelta(days=i)
            if exclude:
                if list_date not in valid_dates:
                    poll.add_answer(text=list_date.strftime("%m/%d (%A)"))
            else:
                poll.add_answer(text=list_date.strftime("%m/%d (%A)"))
        
        await interaction.response.send_message(poll=poll)
        set_document("polls", str(interaction.id), data={"title": title, "poll_id": interaction.id, "guild_id": interaction.guild_id, "user_id": interaction.user.id}) 
        
    @app_commands.command(name="poll_default", description="Replies with a Poll!")
    async def poll_default(self, interaction: discord.Interaction, title: str):
        if not title:
            await interaction.response.send_message("Please provide a title for the poll.")
            return
        
        set_document("polls", str(interaction.id), data={"title": title, "poll_id": interaction.id, "guild_id": interaction.guild_id, "user_id": interaction.user.id}) 
                
        curr_date = datetime.now()
        hours_left_in_day = 24 - curr_date.hour
        today = datetime(curr_date.year, curr_date.month, curr_date.day + 1)
        next_7_days = [today + timedelta(days=i) for i in range(7)]
        
        poll = discord.Poll(question=title, duration=timedelta(hours=hours_left_in_day), multiple=True )
        for day in next_7_days:
            poll.add_answer(text=day.strftime('%d/%m/%Y'))
        message = await interaction.response.send_message(poll=poll)
        self.polls.append(message)
         
    @app_commands.command(name="poll_end", description="Ends the current poll")
    async def poll_end(self, interaction: discord.Interaction, user: discord.Member=None):
        polls = get_by_guild_and_user(interaction.guild_id, interaction.user.id)
        

async def setup(bot):
    await bot.add_cog(Poll(bot))