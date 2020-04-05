"""
Inventory tool object

--

Author : DrLarck

Last update : 05/04/20 by DrLarck
"""

# util
from utility.graphic.embed import CustomEmbed
from utility.graphic.icon import GameIcon


class ToolInventory:

    def __init__(self, client):
        # Public
        self.client = client

        # Private
        self.__embed = CustomEmbed()
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
                                                            WHERE player_id = $1;
                                                            """, [player.id])

        collection = len(player_characters)
        dragonstone = await player.resource.get_dragonstone()
        zeni = await player.resource.get_zeni()

        # Setup the embed
        self.__embed = await self.__embed.setup(self.client, title=f"{player.name}'s inventory",
                                                thumbnail_url=player.avatar)

        # Embed fields
        self.__embed.add_field(name=f"Dragon Stone{self.__icon.dragonstone}",
                               value=dragonstone,
                               inline=True)

        self.__embed.add_field(name=f"Zeni{self.__icon.zeni}",
                               value=zeni,
                               inline=True)

        self.__embed.add_field(name="Collection",
                               value=collection,
                               inline=True)

        return self.__embed
