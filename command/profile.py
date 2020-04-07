"""
Profile command

--

Author : DrLarck

Last update : 07/04/20 by DrLarck
"""

import discord

from discord.ext import commands

# util
from utility.entity.player import Player
from utility.command.checker import CommandChecker
from utility.graphic.embed import CustomEmbed
from utility.interactive.button import Button


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
        # If no target is provided
        # The player is the message author
        if target is None:
            player = Player(self.client, context.message.author)

        # If the target is provided
        # The player is the target
        else:
            player = Player(self.client, target)

        embed = CustomEmbed()

        # Initialize embed's information
        level = await player.experience.get_player_level()

        # Setup the embed
        embed = await embed.setup(self.client, title=f"{player.name}'s profile", thumbnail_url=player.avatar)

        embed.add_field(name=":star:Level", value=level, inline=True)

        # Display the profile
        profile = await context.send(embed=embed)

        # Buttons
        # Add the button to switch to the inventory panel
        button = Button(self.client, profile)
        button_ = ['🛍']

        await button.add(button_)


def setup(client):
    client.add_cog(CommandProfile(client))
