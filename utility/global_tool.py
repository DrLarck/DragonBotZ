"""
Global tools

--

Author : DrLarck

Last update : 05/09/20 by DrLarck
"""

from string import ascii_letters


class GlobalTool:

    @staticmethod
    async def get_rarity_value(rarity_str):
        """
        Return the rarity value based on the rarity str

        :param rarity_str: (`str`)

        --

        :return: `int` or `None` if not found
        """

        # Init
        rarity = None

        # Get the rarity value
        rarity_str = rarity_str.lower()
        rarity_str = rarity_str.strip(' ')

        if rarity_str == 'n':
            rarity = 0

        elif rarity_str == 'r':
            rarity = 1

        elif rarity_str == "sr":
            rarity = 2

        elif rarity_str == "ssr":
            rarity = 3

        elif rarity_str == "ur":
            rarity = 4

        elif rarity_str == "lr":
            rarity = 5

        return rarity

    @staticmethod
    async def generate_unique_id(reference):
        """
        Generate a unique id from the reference

        :param reference: (`int`)

        --

        :return: `str`
        """

        # Init
        letters = ascii_letters

        # Generation
        # First of all, store the highest value in 'number'
        number = int(reference / pow(52, 4))
        reference -= number * pow(52, 4)

        # Then deal the value with the letters
        # Each letter can store (52^index - 1) values
        # The first_letter (tier 1) can handle 52 values
        first_letter = int(reference / pow(52, 3))
        reference -= first_letter * pow(52, 3)

        second_letter = int(reference / pow(52, 2))
        reference -= second_letter * pow(52, 2)

        third_letter = int(reference / 52)
        reference -= third_letter * 52

        fourth_letter = reference

        # Get the unique id
        id_ = f"{letters[fourth_letter]}{letters[third_letter]}{letters[second_letter]}{letters[first_letter]}{number}"

        return id_
    
    @staticmethod
    async def get_player_premium_resource_bonus(player):
        """Generate a value which represent the % bonus to resource gain for premium
        players


        @param Player player

        --

        @return float"""

        bonus = 1

        # Retrieve player's premium data
        premium = await player.get_premium_data()

        # If the player is premium
        if premium["premium"]:
            tier = premium["tier"]
            
            # +15 % per tier
            # 100 % lv6
            # 130 % lv7
            if tier == 1:
                bonus = 1.15
            
            elif tier == 2:
                bonus = 1.3
            
            elif tier == 3:
                bonus = 1.45
            
            elif tier == 4:
                bonus = 1.6
            
            elif tier == 5:
                bonus = 1.75
            
            elif tier == 6:
                bonus = 2
            
            elif tier >= 7:
                bonus = 2.3

        return bonus
