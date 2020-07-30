"""Allow the player to train his characters

--

@author DrLarck

@update 30/07/20 by DrLarck"""

from discord.ext import commands

# util
from utility.command.checker import CommandChecker
from utility.command.tool.tool_train import ToolTrain

from utility.entity.player import Player
from utility.entity.CPU import CPU
from utility.entity.combat import Combat


class CommandTrain(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.tool   = ToolTrain(self.client)

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.check(CommandChecker.not_fighting)
    @commands.check(CommandChecker.has_team)
    async def train(self, context):
        """Allow the player to train his characters"""

        player = Player(context, self.client, context.message.author)
        cpu    = CPU(context, self.client, context.message.author)

        # Set the CPU's team
        opponent_team, level_range = await self.tool.generate_opponent_team(player)
        
        await cpu.set_team(opponent_team, level_range)

        combat = Combat(self.client, context, player, cpu)

        # Run the combat
        winner = await combat.run()
        

def setup(client):
    client.add_cog(CommandTrain(client))
