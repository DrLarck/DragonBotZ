"""Allow the player to start a mission or have a preview of it

--

@author DrLarck

@update 07/08/20 by DrLarck"""

from discord.ext import commands

# util
from utility.command.checker import CommandChecker
from utility.command.tool.tool_mission import ToolMission
from utility.entity.player import Player
from utility.entity.mission import MissionGetter
from utility.entity.combat import Combat
from utility.entity.CPU import CPU


class CommandMission(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.getter = MissionGetter()
    
    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.group(invoke_without_command=True)
    async def mission(self, context):
        """Allow the player to display a list of available missions"""

        tool   = ToolMission(self.client, context)
        player = Player(context, self.client, context.message.author)

        await tool.mission_manager(player)
    
    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.check(CommandChecker.not_fighting)
    @commands.check(CommandChecker.has_team)
    @mission.command()
    async def start(self, context, index):
        """Allows the player to start a mission"""

        mission = await self.getter.get_mission(index)

        # If the mission has been found, start the fight
        if mission is not None:
            player_a = Player(context, self.client, context.message.author)
            player_b = CPU(context, self.client, context.message.author)
            
            # Setup the CPU
            player_b.name = mission.name
            await player_b.set_team(
                mission.opponent,
                [mission.opponent_lvl, mission.opponent_lvl]
            )

            combat = Combat(
                self.client, context, player_a, player_b
            )

            # Start the mission
            winner = await combat.run()

            # Check who won it
            if winner == player_a:
                rewards = await mission.send_rewards(context, player_a)

                await context.send(f"🏆 **{player_a.name}** won the fight ! Here are your rewards : {rewards}")

        else:
            await context.send("Mission not found")
        

def setup(client):
    client.add_cog(CommandMission(client))
