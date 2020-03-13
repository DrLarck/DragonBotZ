"""
Moderation commands

--

Author : DrLarck

Last update : 13/03/20 by DrLarck
"""

from discord.ext import commands


class CommandModeration(commands.Cog):

    def __init__(self, client):
        # Public
        self.client = client

    # Command
    @commands.command()
    async def test(self, context):
        await context.send("This is a test")


def setup(client):
    client.add_cog(CommandModeration(client))
