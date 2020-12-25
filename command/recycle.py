"""Recycling command

@author DrLarck

@update 25/12/20 by DrLarck"""

import asyncio

from discord.ext import commands

# util
from utility.command.checker import CommandChecker
from utility.global_tool import GlobalTool
from utility.entity.player import Player
from utility.graphic.icon import GameIcon
from utility.command.tool.tool_shop import ToolShop


class CommandRecycle(commands.Cog):

    def __init__(self, client):
        self.client = client

        # Recycling reward
        self.__n = 0.1
        self.__r = 0.3
        self.__sr = 0.5
        self.__ssr = 0.8
        self.__ur = 2
        self.__lr = 5

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command()
    async def recycle(self, context, rarity=None):
        """Allows the player to recycle his characters"""

        tool = GlobalTool()
        player = Player(context, self.client, context.message.author)
        characters = []
        generated_shards = 0
        deleted_amount = 0

        # Get the rarity value if specified
        if rarity is not None:
            rarity = await tool.get_rarity_value(rarity)
            
            if rarity is None:
                await context.send(f":x: Unknown rarity `{rarity}`")
                return

        # If the rarity passed is correct
        if rarity is not None:
            # Get all the character with the passed rarity
            characters = await self.client.database.fetch_row("""
                                                              SELECT reference, character_rarity
                                                              FROM character_unique
                                                              WHERE character_rarity = $1
                                                              AND character_owner_id = $2
                                                              AND locked = false;
                                                              """,[rarity, player.id])

        else:
            characters = await self.client.database.fetch_row(
                """
                SELECT reference, character_rarity, character_unique_id
                FROM character_unique
                WHERE character_owner_id = $1
                AND locked = false;
                """, [player.id]
            )    
        
        # Generate and delete characters
        deleted_amount = len(characters)
        shop = ToolShop(self.client, context)

        # Get the transaction object
        transaction = await self.client.database.get_transaction()
        await transaction.start()
        
        for character in characters:
            await asyncio.sleep(0)

            reference = character[0]
            rarity = character[1]
            unique = character[2]

            # If the character is not in the shop
            if not await shop.find_character(unique):
                if rarity == 0:
                    generated_shards += self.__n
                
                elif rarity == 1:
                    generated_shards += self.__r
                
                elif rarity == 2:
                    generated_shards += self.__sr
                
                elif rarity == 3:
                    generated_shards += self.__ssr
                
                elif rarity == 4:
                    generated_shards += self.__ur
                
                elif rarity == 5:
                    generated_shards += self.__lr
                
                # Remove the character from the character unique
                await self.client.database.execute(
                    """
                    DELETE 
                    FROM character_unique
                    WHERE reference = $1;
                    """, [reference]
                )
            
            else:
                deleted_amount -= 1

        # Close the transaction
        await transaction.commit()

        # Add the shards to the player's resources
        player_shard = await self.client.database.fetch_value(
            """
            SELECT player_dragonstone_shard
            FROM player_resource
            WHERE player_id = $1;
            """, [player.id]
        )

        new_shard = player_shard + generated_shards

        await self.client.database.execute(
            """
            UPDATE player_resource
            SET player_dragonstone_shard = $1
            WHERE player_id = $2;
            """, [new_shard, player.id]
        )

        # Send message
        await context.send(f"♻️ You have recycled **{deleted_amount:,}** characters and generated **{generated_shards:.2f}** {GameIcon().dragonstone}")

        # Add the dragonstone to the player
        added_ds = int(await player.resource.get_dragonstone_shard())
        await player.resource.add_dragonstone(added_ds)

        # Remove the shard
        await player.resource.remove_dragonstone_shard(added_ds)


def setup(client):
    client.add_cog(CommandRecycle(client))
