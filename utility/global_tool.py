"""
Global tools

--

Author : DrLarck

Last update : 07/04/20 by DrLarck
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
