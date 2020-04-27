"""
Represents the combat object

--

Author : DrLarck

Last update : 27/04/20 by DrLarck
"""


class Combat:

    def __init__(self):
        # Public
        # Player
        self.team_a, self.team_b = [], []

        # Private
        self.__combat_tool = CombatTool(self)

    # Public
    async def run_turn(self, player_index):
        """
        Run the player's turn

        :param player_index: (`int`)

        --

        :return: `None`
        """

        # Init
        player_team = await self.__combat_tool.get_player_team_by_index(player_index)


        return


class CombatTool:

    def __init__(self, combat):
        """
        :param combat: (`Combat`)
        """

        # Public
        self.combat = combat

    # Public
    async def init_teams(self):
        """
        Init the players team

        :return: `None`
        """

        return

    async def get_player_team_by_index(self, player_index):
        """
        Return the player team by player index

        :param player_index: (`int`)

        --

        :return: `list` of `Character`
        """

        if player_index == 0:
            return self.combat.team_a

        else:
            return self.combat.team_b
