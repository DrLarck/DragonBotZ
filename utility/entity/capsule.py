"""Represent a capsule

--

Author : DrLarck

Last update : 13/04/20 by DrLarck"""

import random


class Capsule:

    def __init__(self, context, client, player):
        """:param context: (`discord.ext.commands.Context`)
           
           :param client: (`discord.ext.commands.Bot`)

           :param player: (`Player`)"""

        # Public
        self.client = client
        self.context = context
        self.player = player

        # Info
        self.name = ""
        self.icon = ""

        # Private
        # Rewards
        self.__dragonstone = 0
        self.__zeni = 0
        self.__experience = 0
        self.__item = []

        # Rate
        # As %
        # One of the rates must be 100 as we eliminate
        self.__rate_dragonstone = 0
        self.__rate_zeni = 0
        self.__rate_experience = 0
        self.__rate_item = 0

    # Public method
    async def open(self):
        """Open the capsule and send the reward to the player

        --

        :return: `None`"""

        # Get the player's roll
        roll = random.uniform(0, 100)

        # Check if the item list is not empty
        if len(self.__item) > 0:
            # Check if the player has loot a training item
            if roll <= self.__rate_item:
                item = random.choice(self.__item)
                
        return
