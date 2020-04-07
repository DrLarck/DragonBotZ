"""
Box command

--

Author : Drlarck

Last update : 07/04/20 by DrLarck
"""

from discord.ext import commands

# util
from utility.command.checker import CommandChecker


class CommandBox(commands.Cog):

    def __init__(self, client):
        # Public
        self.client = client

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.command()
    async def box(self, context):
        await context.send("Test")


def setup(client):
    client.add_cog(CommandBox(client))
