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

        self.resource = PlayerResource()


class PlayerResource:

    def __init__(self, player):
        # Public
        self.player = player

    # Public Method
    async def get_resources(self):
        """
        Get the player's resources

        --

        :return: `list` | Index : 0 Dragon stones, 1 Zenis
        """

        # Init
        database = Database()

        resources = await database.fetch_value("""
                                               SELECT player_dragonstone, player_zenis 
                                               FROM player_resource 
                                               WHERE player_id = $1;""", [self.player.id])

        return resources
