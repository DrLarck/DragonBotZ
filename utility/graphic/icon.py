"""
Game icon

--

Author : DrLarck

Last update : 19/03/20 by DrLarck
"""


class GameIcon:

    def __init__(self):
        # Public
        # Resource
        self.dragonstone = "<:dragonstone:594954189579354112>"
        self.zeni = "<:zenis:594954191999336514>"

        # Private
        self.__rarity = [
                        "<:N_:529974556379840513>", "<:R_:529974570803920897>", "<:SR:554333952006029312>",
                        "<:SSR:554333988399874058>", "<:UR:554334033413275649>", "<:LR:554333076285816853>"
                        ]
        self.__type = [
                      
                      ]

    # Public
    async def get_rarity_icon(self, rarity_value):
        """
        Get the rarity icon

        :param rarity_value: (`int`)

        --

        :return: `str`
        """

        return self.__rarity[rarity_value]

    async def get_type_icon(self, type_value):
        """
        Get the type icon

        :param type_value: (`int`)

        --

        :return: `str`
        """

        return self.__type[type_value]
