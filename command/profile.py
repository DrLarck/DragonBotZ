"""
Profile command

--

Author : DrLarck

Last update : 06/09/20 by DrLarck
"""

import discord

from discord.ext import commands

# util
from utility.entity.player import Player
from utility.command.checker import CommandChecker
from utility.graphic.embed import CustomEmbed
from utility.interactive.button import Button

# tool
from utility.command.tool.tool_inventory import ToolInventory
from utility.command.tool.tool_time import ToolTime


class CommandProfile(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.command()
    async def profile(self, context, target: discord.Member = None):

        # Log
        await self.client.logger.log(context)

        # Init
        # Get the command caller
        caller = Player(context, self.client, context.message.author)
        timer  = ToolTime()

        # If no target is provided
        # The player is the message author
        if target is None:
            player = Player(context, self.client, context.message.author)

        # If the target is provided
        # The player is the target
        else:
            player = Player(context, self.client, target)

        embed = CustomEmbed()

        # Initialize embed's information
        power        = await player.experience.get_player_power()
        hr_combo     = await player.time.get_hourly_combo()
        day_combo    = await player.time.get_daily_combo()
        premium_data = await player.get_premium_data()

        # Check if the player is premium
        # and calculate info
        is_premium = premium_data["premium"]

        premium_time   = 0
        premium_tier   = 0
        premium_remain = 0

        # Setup the embed
        embed = await embed.setup(self.client, title=f"{player.name}'s profile", thumbnail_url=player.avatar)
        
        # Power
        embed.add_field(
            name=":star: Power", 
            value=power, 
            inline=True
        )

        # Hr combo
        embed.add_field(
            name="⌛ Hourly combo",
            value=hr_combo,
            inline=True
        )

        # Daily combo
        embed.add_field(
            name="☀️ Daily combo",
            value=day_combo,
            inline=True
        )

        # Manage premium field
        if is_premium:
            premium_time   = premium_data["total_month"]
            premium_tier   = premium_data["tier"]
            premium_remain = await timer.convert_time(premium_data["remaining"])

            embed.add_field(
                name="👑 Premium",
                value=f"Tier **{premium_tier:,}** for **{premium_time:,}** months, **{premium_remain}** remaining"
            )
        
        else:
            embed.add_field(
                name="👑 Premium",
                value="Not premium"
            )

        # Display the profile
        profile = await context.send(embed=embed)

        # Stop condition
        stop = False
        count = 0
        pressed = None

        while not stop:
            # If no button has been pressed
            if count > 0 and pressed is None:
                break

            # Profile buttons
            # Get the pressed button
            # Add the button to switch to the inventory panel
            button = Button(self.client, profile)
            profile_button = ['📦']

            await button.add(profile_button)
            pressed = await button.get_pressed(profile_button, caller)

            # Always go back to the profile panel
            # If the pressed button is the inventory button
            if pressed == profile_button[0]:
                # Display the inventory
                inventory_tool = ToolInventory(self.client)
                inventory_embed = await inventory_tool.get_inventory_embed(player)

                # Replace the profile display by the inventory embed
                await profile.delete()
                inventory = await context.send(embed=inventory_embed)

                # Add a button to go back to the profile
                inventory_button = ['👤']

                # Redefine the button's message
                button = Button(self.client, inventory)
                await button.add(inventory_button)

                # Get the inventory pressed button
                pressed = await button.get_pressed(inventory_button, caller)

                # If the pressed button is the profile button
                if pressed == inventory_button[0]:
                    # Replace the inventory embed by the profile embed
                    await inventory.delete()

                    # Display the profile
                    profile = await context.send(embed=embed)

            count += 1


def setup(client):
    client.add_cog(CommandProfile(client))
