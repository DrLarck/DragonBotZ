"""
Inventory command

--

Author : DrLarck

Last update : 05/04/20 by DrLarck
"""

from discord.ext import commands

# util
from utility.entity.player import Player

# tool
from utility.command.tool.tool_inventory import ToolInventory


class CommandInventory(commands.Cog):

    def __init__(self, client):
        self.client = client

        # Private
        self.__tool = ToolInventory(self.client)

    @commands.command()
    async def inventory(self, context):
        # Init
        player = Player(self.client, context.message.author)
        inventory = await self.__tool.get_inventory_embed(player)

        await context.send(embed=inventory)


def setup(client):
    client.add_cog(CommandInventory(client))
