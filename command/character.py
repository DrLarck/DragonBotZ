"""Character tool for the player like lock/unlock and info displaying

@author DrLarck

@update 1/11/20 by DrLarck"""

from discord.ext import commands

# util
from utility.entity.player import Player
from utility.command.checker import CommandChecker
from utility.command.tool.tool_help import ToolHelp


class CommandCharacter(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.group(invoke_without_command=True)
    async def character(self, context):
        """Display the character help"""

        player = Player(context, self.client, context.message.author)
        help = ToolHelp(self.client, context, player)

        await context.send(embed=await help.get_detailed_help_for(1, "character"))
    
    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @character.group(invoke_without_command=True)
    async def lock(self, context, unique_id):
        """Allows the player to lock a character he owns"""

        player = Player(context, self.client, context.message.author)

        # If the player owns the character
        if await player.item.has_character(unique_id):
            await self.client.database.execute(
                """
                UPDATE character_unique
                SET locked = true
                WHERE character_unique_id = $1;
                """, [unique_id]
            )

            await context.send("✅ You have successfully locked the character")
        
        else:
            await context.send(":x: You do not own this character")
    
    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @lock.command()
    async def all(self, context):
        """Allows the player to lock all his characters"""

        player = Player(context, self.client, context.message.author)

        await self.client.database.execute(
            """
            UPDATE character_unique
            SET locked = true
            WHERE character_owner_id = $1;
            """, [player.id]
        )

        await context.send("✅ You have successfully locked your characters")
    
    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @character.group(invoke_without_command=True)
    async def unlock(self, context, unique_id):
        """Allows the player to unlock a character he owns"""

        player = Player(context, self.client, context.message.author)

        # If the player owns the character
        if await player.item.has_character(unique_id):
            await self.client.database.execute(
                """
                UPDATE character_unique
                SET locked = false
                WHERE character_unique_id = $1;
                """, [unique_id]
            )

            await context.send("✅ You have successfully unlocked the character")
        
        else:
            await context.send(":x: You do not own this character")
    
    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @unlock.command()
    async def all(self, context):
        """Allows the player to lock all his characters"""

        player = Player(context, self.client, context.message.author)

        await self.client.database.execute(
            """
            UPDATE character_unique
            SET locked = false
            WHERE character_owner_id = $1;
            """, [player.id]
        )

        await context.send("✅ You have successfully unlocked your characters")


def setup(client):
    client.add_cog(CommandCharacter(client))
