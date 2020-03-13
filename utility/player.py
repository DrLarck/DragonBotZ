"""
Player object

--

Author : DrLarck

Last update : 13/03/20 by DrLarck
"""


class Player:

    def __init__(self, user):
        # Public
        self.name = user.name
        self.id = user.id

        self.resource = PlayerResource()


class PlayerResource:

    def __init__(self):
        self.__dragonstone = 0
        self.__zeni = 0

