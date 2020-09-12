"""Trade command

--

@author DrLarck

@update 12/09/20 by DrLarck"""

import discord
from discord.ext import commands

# tool
from utility.command.tool.tool_trade import ToolTrade

# util
from utility.command.checker import CommandChecker
from utility.entity.player import Player


class CommandTrade(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.tool   = ToolTrade(self.client)

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.command()
    async def trade(self, context, target: discord.Member):
        """Allows player to trade items"""

        player_a = Player(context, self.client, ctx.message.author)
        player_b = Player(context, self.client, target)

        await self.tool.trade(context, player_a, player_b)


def setup(client):
    client.add_cog(CommandTrade(client))
