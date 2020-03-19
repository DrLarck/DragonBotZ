"""
Character getter

--

Author : DrLarck

Last update : 19/03/20 by DrLarck
"""

# util
from utility.database import Database
from utility.entity.character import Character


class CharacterGetter:

    def __init__(self):
        # Private
        self.__database = Database()

    # Public
    async def get_reference_character(self, reference):
        """
        Get a base character

        :param reference: (`int`)

        --

        :return: `Character` or `None`
        """

        # Init
        character = Character()

        # Get the character from the database
        data = await self.__database.fetch_row("""
                                              SELECT * FROM character_reference 
                                              WHERE reference = $1; 
                                              """, [reference])

        if len(data) > 0:  # Character found
            data = data[0]

            # Get a character instance according to the data we just fetched
            character = await character.generate(char_id=data[0], name=data[1], type_value=data[2],
                                                 rarity_value=data[3], card=data[4], health=data[5],
                                                 physical=data[6])

            return character

        else:  # Character not found
            print(f"Character #{reference} not found.")
            return
