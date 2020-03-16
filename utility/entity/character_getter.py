"""
Character getter

--

Author : DrLarck

Last update : 16/03/20 by DrLarck
"""

# util
from utility.database import Database


class CharacterGetter:

    def __init__(self):
        # Private
        self.__database = Database()

    # Public
    async def get_base_character(self, base_id):
        """
        Get a base character

        :param base_id: (`int`)

        --

        :return: `Character`
        """

        # Init


