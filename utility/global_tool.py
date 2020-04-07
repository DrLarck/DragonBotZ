"""
Global tools

--

Author : DrLarck

Last update : 07/04/20 by DrLarck
"""


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
