"""
Player object

--

Author : DrLarck

Last update : 14/03/20 by DrLarck
"""

from utility.database import Database


class Player:

    def __init__(self, user):
        # Public
        self.name = user.name
        self.id = user.id

        self.resource = PlayerResource(self)


class PlayerResource:

    def __init__(self, player):
        # Private
        self.__database = Database()

        # Public
        self.player = player

    # Public Method
    async def get_resources(self):
        """
        Get the player's resources

        --

        :return: `list` | Index : 0 Dragon stones, 1 Zenis
        """

        resources = await self.__database.fetch_row("""
                                                    SELECT player_dragonstone, player_zeni 
                                                    FROM player_resource 
                                                    WHERE player_id = $1;
                                                    """, [self.player.id])

        return resources[0]

    async def get_dragonstone(self):
        """
        Get the player's dragon stone amount

        --

        :return: `int`
        """

        dragonstone = await self.__database.fetch_value("""
                                                        SELECT player_dragonstone 
                                                        FROM player_resource 
                                                        WHERE player_id = $1;
                                                        """, [self.player.id])

        return dragonstone

    async def get_zeni(self):
        """
        Get the player's zeni amount

        --

        :return: `int`
        """

        zeni = await self.__database.fetch_value("""
                                                SELECT player_zeni 
                                                FROM player_resource 
                                                WHERE player_id = $1;
                                                """, [self.player.id])

        return zeni
