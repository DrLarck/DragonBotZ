"""
Represents the combat object

--

Author : DrLarck

Last update : 27/04/20 by DrLarck
"""

import random


class Combat:

    def __init__(self):
        # Public
        # Player
        self.player_a, self.player_b = None, None
        self.team_a, self.team_b = [], []

        # Private
        self.__combat_tool = CombatTool(self)

    # Public
    async def run(self):
        """
        Run the combat

        --

        :return: `Player` as winner
        """



        return

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

        # Get the team for the player
        # A
        if self.combat.player_a is not None:
            self.combat.team_a = await self.combat.player_a.combat.get_team()

        # B
        if self.combat.player_b is not None:
            self.combat.team_b = await self.combat.player_b.combat.get_team()

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

    async def define_play_order(self):
        """
        Redefine player_a and player_b to define a play order

        --

        :return: `None`
        """

        # Roll the first player
        roll = random.randint(0, 1)

        # If the first player to play is the player b
        if roll == 1:
            self.combat.player_a = self.combat.player_b
            self.combat.player_b = self.combat.player_a

        # else doesn't change anything

        return
