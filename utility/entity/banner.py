"""
Banner object

--

Author : DrLarck

Last update : 20/03/20 by DrLarck
"""

import asyncio


class Banner:

    def __init__(self):
        # Public
        self.name = ""
        self.image = ""
        self.characters = []
        self.sorted = False

        # Private
        self.__lr = []
        self.__ur = []
        self.__ssr = []
        self.__sr = []
        self.__r = []
        self.__n = []

        # Droprate as %
        self.__lr_droprate = 0.01
        self.__ur_droprate = 3
        self.__ssr_droprate = 15
        self.__ssr_droprate = 33
        self.__lr_droprate = 50
        self.__n_droprate = 100

    # Public
    async def sort(self):
        """
        Sort the banner

        --

        :return: `None`
        """

        if self.sorted is False:
            # Sort the characters
            for character in self.characters:
                await asyncio.sleep(0)

                # Put the character in the LR list
                if character.rarity.value == 5:
                    self.__lr.append(character)

                # Put the character in the UR list
                elif character.rarity.value == 4:
                    self.__ur.append(character)

                elif character.rarity.value == 3:
                    self.__ssr.append(character)

                elif character.rarity.value == 2:
                    self.__sr.append(character)

                elif character.rarity.value == 1:
                    self.__r.append(character)

                elif character.rarity.value == 0:
                    self.__n.append(character)

                self.sorted = True

        return
