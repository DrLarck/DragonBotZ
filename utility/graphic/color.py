"""
Game color object

--

Author : DrLarck

Last update : 28/04/20 by DrLarck
"""


class GameColor:

    def __init__(self):
        # Public
        # Rarity
        self.lr = 0xd90e82
        self.ur = 0x0b68f3
        self.ssr = 0xfcdc09
        self.sr = 0xfe871a
        self.r = 0xdcdede
        self.n = 0xad5f25

        # Combat
        self.player_a = 0x009dff
        self.player_b = 0xff0000

    # Public
    async def get_rarity_color(self, rarity):
        """
        Return the rarity color

        :param rarity: (`int`)

        --

        :return: `int` as hexadecimal value
        """

        if rarity == 0:
            return self.n

        elif rarity == 1:
            return self.r

        elif rarity == 2:
            return self.sr

        elif rarity == 3:
            return self.ssr

        elif rarity == 4:
            return self.ur

        elif rarity == 5:
            return self.lr
