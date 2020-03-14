"""
Character object

--

Author : Drlarck

Last update : 14/03/20 by DrLarck
"""


class Character:

    def __init__(self):
        # Public
        self.name = ""
        self.id = 0
        self.level = 1

        self.image = CharacterImage()
        self.type = CharacterType()
        self.rarity = CharacterRarity()
        self.health = CharacterHealth()
        self.ki = CharacterKi()


class CharacterImage:

    def __init__(self):
        # Public
        self.card = ""
        self.thumbnail = ""
        self.icon = ""


class CharacterType:

    def __init__(self):
        # Public
        self.value = 0
        self.icon = ""


class CharacterRarity:

    def __init__(self):
        # Public
        self.value = 0
        self.icon = ""


class CharacterHealth:

    def __init__(self):
        # Public
        self.maximum = 0
        self.current = 0


class CharacterKi:

    def __init__(self):
        # Public
        self.maximum = 0
        self.current = 0
