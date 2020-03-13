"""
Start command

--

Author : DrLarck

Last update : 13/03/20 by DrLarck
"""

from discord.ext import commands

class CommandStart(commands.Cog)

    def __init__(self, client):
        # Public
        self.client = client


def setup(client):
    client.add_cog(CommandStart(client))