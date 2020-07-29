"""Allow the player to manage his team

--

@author DrLarck

@update 29/07/20 by DrLarck"""

from discord.ext import commands
from utility.command.checker import CommandChecker
from utility.entity.player import Player


class CommandTeam(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.group(invoke_without_command=True)
    async def team(self, context):
        """Allow the player to display his team"""

        player = Player(context, self.client, context.message.author)

def setup(client):
    client.add_cog(CommandTeam(client))
