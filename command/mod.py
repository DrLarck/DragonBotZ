"""
Moderation commands

--

Author : DrLarck

Last update : 13/03/20 by DrLarck
"""

from discord.ext import commands

# util
from utility.logger.command_logger import CommandLogger
from utility.command.checker import CommandChecker
from utility.player import Player


class CommandModeration(commands.Cog):

    def __init__(self, client):
        # Public
        self.client = client

    # Command
    @commands.check(CommandChecker.register)
    @commands.check(CommandChecker.no_dm)
    @commands.command()
    async def test(self, context):

        # Init
        await CommandLogger().log(context)

        player = Player(context.message.author)

        resources = await player.resource.get_resources()

        print(resources[0], resources[1])


def setup(client):
    client.add_cog(CommandModeration(client))
