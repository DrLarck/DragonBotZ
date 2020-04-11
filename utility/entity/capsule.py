"""Represent a capsule"""

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

            return
        
        async def display(self, reward_type, reward):
            """Send a message using `context` according to the reward type and the reward

            :param reward_type: (`int`)

            :param reward: (`int`)

            --

            :return: `None`"""
            
            return
