"""Help command

--

@author DrLarck

@update 08/08/20 by DrLarck"""

from discord.ext import commands

#util
from utility.command.checker import CommandChecker
from utility.command.tool.tool_help import ToolHelp
from utility.entity.player import Player


class CommandHelp(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.check(CommandChecker.game_ready)
    @commands.command()
    async def help(self, context, command=None):
        """Display the help"""

        player = Player(context, self.client, context.message.author)
        tool   = ToolHelp(self.client, context, player)

        if command is None:
            await tool.help_manager()
        
        else:
            await tool.help_manager(command)


def setup(client):
    client.add_cog(CommandHelp(client))
