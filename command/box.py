"""
Box command

--

Author : Drlarck

Last update : 07/04/20 by DrLarck
"""

from discord.ext import commands

# util
from utility.command.checker import CommandChecker
from utility.entity.player import Player

# tool
from utility.command.tool.tool_box import ToolBox


class CommandBox(commands.Cog):

    def __init__(self, client):
        # Public
        self.client = client

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.command()
    async def box(self, context):
        # Log
        await self.client.logger.log(context)
        
        # Init
        player = Player(self.client, context.message.author)
        tool = ToolBox(self.client, context)

        await tool.box_manager(player)


def setup(client):
    client.add_cog(CommandBox(client))
