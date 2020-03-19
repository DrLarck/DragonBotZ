"""
Character getter

--

Author : DrLarck

Last update : 19/03/20 by DrLarck
"""

import asyncio

# util
from utility.database import Database
from utility.entity.character import Character


class CharacterGetter:

    # Private
    __database = Database()
    __cache = []
    __cache_ok = False  # Indicates if the cache has already been filled

    # Public
    async def set_cache(self):
        """
        Set the character cache

        --

        :return: `None`
        """

        if self.__cache_ok is False:
            data = await self.__database.fetch_row("""
                                                 SELECT *
                                                 FROM character_reference
                                                 ORDER BY reference;
                                                 """)

            if len(data) > 0:
                # Storing each character in the cache as Character objects
                for character in data:
                    await asyncio.sleep(0)

                    character_ = await Character().generate(char_id=character[0], name=character[1],
                                                            type_value=character[2], rarity_value=character[3],
                                                            card=character[4], health=character[5],
                                                            physical=character[6])

                    self.__cache.append(character_)
                    print(f"Append {character_.name}")

                # Cache has been filled
                self.__cache_ok = True
                print("Character Cache : DONE")

        else:  # The cache has already been filled
            print("Character Cache : The cache has already been filled.")

        return

    async def get_reference_character(self, reference):
        """
        Get a base character

        :param reference: (`int`)

        --

        :return: `Character` or `None`
        """

        # Get the character from the cache
        if reference > 0 and reference < len(self.__cache):
            print(self.__cache)

        else:
            print(f"Character {reference} not found.")
            return None
