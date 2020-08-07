"""Allow the player to start a mission or have a preview of it

--

@author DrLarck

@update 07/08/20 by DrLarck"""

from discord.ext import commands

# util
from utility.command.checker import CommandChecker
from utility.command.tool.tool_mission import ToolMission


class CommandMission(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.group(invoke_without_command=True)
    async def mission(self, context):
        """Allow the player to display a list of available missions"""

        tool = ToolMission(self.client, context)

        await tool.mission_manager()
        

def setup(client):
    client.add_cog(CommandMission(client))
