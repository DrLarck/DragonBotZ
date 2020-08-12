"""Shop command

--

@author DrLarck

@update 12/08/20 by DrLarck"""

from discord.ext import commands

# util
from utility.command.checker import CommandChecker
from utility.command.tool.tool_shop import ToolShop
from utility.entity.player import Player
from utility.command.tool.tool_help import ToolHelp


class CommandShop(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.group(invoke_without_command=True)
    async def shop(self, context):
        """Displays the shop help"""

        player = Player(context, self.client, context.message.author)
        help = ToolHelp(self.client, context, player)

        await context.send(embed=await help.get_detailed_help_for(1, "shop"))
    
    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @shop.command()
    async def character(self, context, character_id:int=None):
        """Displays the character shop"""

        player = Player(context, self.client, context.message.author)
        tool = ToolShop(self.client, context)

        await tool.shop_manager(player, character_id=character_id)
        

def setup(client):
    client.add_cog(CommandShop(client))
