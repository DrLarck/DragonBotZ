"""
Game icon

--

Author : DrLarck

Last update : 20/03/20 by DrLarck
"""


class GameIcon:

    def __init__(self):
        # Public
        # Resource
        self.dragonstone = "<:dragonstone:594954189579354112>"
        self.zeni = "<:zenis:594954191999336514>"

        # Private
        self.__rarity = [
                        "<:n_:582922492402860053>", "<:r_:582922493644374047>", "<:sr:582922500409786368>",
                        "<:ssr:582922518650683406>", "<:ur:582922519632281628>", "<:lr:582924249073844231>"
                        ]
        self.__type = [
                      "<:phy:582934077812768769>", "<:int:582934074658783253>", "<:teq:582934078831984665>",
                      "<:agl:582934074197409793>", "<:str:582934078685184000>"
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
