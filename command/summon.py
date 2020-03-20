"""
Summon command

--

Author : DrLarck

Last update : 20/03/20 by DrLarck
"""

from discord.ext import commands


class CommandSummon(commands.Cog):

    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(CommandSummon(client))