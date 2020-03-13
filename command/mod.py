"""
Moderation commands

--

Author : DrLarck

Last update : 13/03/20 by DrLarck
"""

from discord.ext import commands
from utility.logger.command_logger import CommandLogger
from utility.command.checker import CommandChecker


class CommandModeration(commands.Cog):

    def __init__(self, client):
        # Public
        self.client = client

    # Command
    @commands.check(CommandChecker.no_dm)
    @commands.command()
    async def test(self, context, param1, param2, param3):
        await context.send(f"This is a test : {param1} {param2} {param3}")

        await CommandLogger().log(context)


def setup(client):
    client.add_cog(CommandModeration(client))
