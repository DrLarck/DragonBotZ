"""
Profile command

--

Author : DrLarck

Last update : 21/03/20 by DrLarck
"""

from discord.ext import commands


class CommandProfile(commands.Cog):

    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(CommandProfile(client))
