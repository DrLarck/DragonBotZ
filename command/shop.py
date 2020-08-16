"""Shop command

--

@author DrLarck

@update 15/08/20 by DrLarck"""

from discord.ext import commands

# util
from utility.command.checker import CommandChecker
from utility.command.tool.tool_shop import ToolShop
from utility.entity.player import Player
from utility.command.tool.tool_help import ToolHelp


class CommandShop(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Shop displaying
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
    
    # Shop interaction
    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @shop.command()
    async def buy(self, context, type_=None, object_id=None):
        """Alllows the player to buy an item from the shop
        
        Available type_ : 'character'"""

        tool = ToolShop(self.client, context)

        # If the player didn't pass any type, display the help
        if type_ is None:
            player = Player(context, self.client, context.message.author)
            help = ToolHelp(self.client, context, player)

            await context.send(embed=await help.get_detailed_help_for(1, "shop"))
            return
        
        if object_id is None:
            await context.send(":x: You didn't pass any object id")
            return

        # Player asked to buy a character
        if type_.lower() == "character":
            char = await tool.find_character(object_id)
            print(char)

        # Type not found
        else:
            await context.send(":x: Unrecognized item type")



def setup(client):
    client.add_cog(CommandShop(client))
