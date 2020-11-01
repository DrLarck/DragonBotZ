"""
Inventory tool object

--

Author : DrLarck

Last update : 1/11/20 by DrLarck
"""

# util
from utility.graphic.embed import CustomEmbed
from utility.graphic.icon import GameIcon


class ToolInventory:

    def __init__(self, client):
        # Public
        self.client = client

        # Private
        self.__database = self.client.database
        self.__icon = GameIcon()

    # Public
    async def get_inventory_embed(self, player):
        """
        Return an embed message of the player's inventory

        :param player: (`Player`)

        --

        :return: `discord.Embed`
        """

        # Init
        player_characters = await self.__database.fetch_row("""
                                                            SELECT *
                                                            FROM character_unique
                                                            WHERE character_owner_id = $1;
                                                            """, [player.id])

        embed = CustomEmbed()

        collection = len(player_characters)
        dragonstone = await player.resource.get_dragonstone()
        dragonstone_shard = await player.resource.get_dragonstone_shard()
        zeni = await player.resource.get_zeni()

        # Setup the embed
        embed = await embed.setup(self.client, title=f"{player.name}'s inventory",
                                  thumbnail_url=player.avatar)

        # Embed fields
        embed.add_field(name=f"{self.__icon.dragonstone}Dragon Stone",
                        value=f"{dragonstone:,}",
                        inline=True)
        
        embed.add_field(name="♻️Dragon Stone shards",
                        value=f"{dragonstone_shard:.2f}",
                        inline=True)

        embed.add_field(name=f"{self.__icon.zeni}Zeni",
                        value=f"{zeni:,}",
                        inline=True)

        embed.add_field(name="Character",
                        value=f"{collection:,}",
                        inline=True)

        return embed
