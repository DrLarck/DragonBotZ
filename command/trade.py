"""Trade command

--

@author DrLarck

@update 13/09/20 by DrLarck"""

import discord
from discord.ext import commands

# tool
from utility.command.tool.tool_trade import ToolTrade
from utility.command.tool.tool_trade import TradeGetter

# util
from utility.command.checker import CommandChecker
from utility.entity.player import Player


class CommandTrade(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.tool   = ToolTrade(self.client)
        self.getter = TradeGetter()

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.check(CommandChecker.not_fighting)
    @commands.check(CommandChecker.no_dm)
    @commands.check(CommandChecker.not_trading)
    @commands.command()
    async def trade(self, context, target: discord.Member):
        """Allows player to trade items"""

        await self.client.logger.log(context)

        player_a = Player(context, self.client, context.message.author)
        player_b = Player(context, self.client, target)

        # Check if the player_b is in trade
        player_b_trading = await self.getter.is_trading(player_b)

        # If the player b is in trade, just return
        if player_b_trading:
            return

        if player_a.id == player_b.id:
            await context.send(":x: You can't trade with yourself")
            return

        await self.tool.trade(context, player_a, player_b)


def setup(client):
    client.add_cog(CommandTrade(client))
