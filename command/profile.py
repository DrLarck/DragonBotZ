"""
Profile command

--

Author : DrLarck

Last update : 21/03/20 by DrLarck
"""

import discord

from discord.ext import commands

# util
from utility.entity.player import Player
from utility.command.checker import CommandChecker
from utility.graphic.embed import CustomEmbed


class CommandProfile(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
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

        # Initialize embed's informations
        level = player.level
        


def setup(client):
    client.add_cog(CommandProfile(client))
