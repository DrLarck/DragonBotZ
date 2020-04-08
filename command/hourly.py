"""
Hourly command

--

Author : DrLarck

Last update : 08/04/20 by DrLarck
"""

from discord.ext import commands

# util
from utility.command.checker import CommandChecker
from utility.entity.player import Player


class CommandHourly(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.command()
    async def hourly(self, context):
        # Log
        await self.client.logger.log(context)

        # Init
        player = Player(self.client, context.message.author)


def setup(client):
    client.add_cog(CommandHourly(client))