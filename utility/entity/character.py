"""
Character object

--

Author : Drlarck

Last update : 19/03/20 by DrLarck
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

        self.damage = CharacterDamage()
        self.critical = CharacterCritical()

        self.armor = CharacterDefense()
        self.spirit = CharacterDefense()

    # Public method
    async def generate(self, name="", char_id=0, level=1,
                       card="", thumbnail="",
                       type_value=0, rarity_value=0, health=0,
                       ki=0, physical=0, ki_power=0,
                       crit_chance=0, crit_bonus=0, armor_fixed=0,
                       armor_floating=0, spirit_fixed=0, spirit_floating=0):
        """
        Generate a character instance.

        :param name: (`str`)
        :param char_id: (`int`)
        :param level: (`int`)
        :param card: (`url`)
        :param thumbnail: (`url`)
        :param type_value: (`int`)
        :param rarity_value: (`int`)
        :param health: (`int`)
        :param ki: (`int`)
        :param physical: (`int`)
        :param ki_power: (`int`)
        :param crit_chance: (`int`)
        :param crit_bonus: (`int`)
        :param armor_fixed: (`int`)
        :param armor_floating: (`int`)
        :param spirit_fixed: (`int`)
        :param spirit_floating: (`int`)

        --

        :return: `Character`
        """

        # Init all the attributes
        self.name = name
        self.id = char_id
        self.level = level

        self.image.card = card
        self.image.thumbnail = thumbnail

        self.type.value = type_value
        self.rarity.value = rarity_value

        self.health.maximum = health

        self.ki = ki

        self.damage.physical = physical
        self.damage.ki = ki_power

        self.critical.chance = crit_chance
        self.critical.bonus = crit_bonus

        self.armor.fixed = armor_fixed
        self.armor.floating = armor_floating

        self.spirit.fixed = spirit_fixed
        self.spirit.floating = spirit_floating

        # Init sub-attributes

        # Get the icons

        # Return the character

        return self

    async def get_display_card(self):
        """
        Generate a display card of this character

        --

        :return: `discord.Embed`
        """

        # Init
        embed = discord.Embed()



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

    # Public method
    async def init(self):
        """
        Init the current health

        --

        :return: `None`
        """

        self.current = self.maximum

        return

    async def limit(self):
        """
        Avoid the current health to reach a value that is < 0 or higher than the max health

        --

        :return: `None`
        """

        if self.current < 0:
            self.current = 0

        if self.current > self.maximum:
            self.current = self.maximum

        return


class CharacterKi:

    def __init__(self):
        # Public
        self.maximum = 0
        self.current = 0

    # Public method
    async def limit(self):
        """
        Avoid the current ki value to reach a value that is < 0 or higher than maximum

        --

        :return: `None`
        """

        if self.current < 0:
            self.current = 0

        if self.current > self.maximum:
            self.current = self.maximum

        return


class CharacterDamage:

    def __init__(self):
        # Public
        self.physical = 0
        self.ki = 0

        # Private
        # This represents the difference in % between the max value and the min value
        # For example, if the range is set to 10 and the max value is 100
        # The min value would be 90 and max 100
        self.__physical_range = 10
        self.__ki_range = 10

    # Public method
    async def get_physical_min(self):
        """
        Return the minimal value of the physical damage range

        --

        :return: `int`
        """

        minimal = self.physical * (1 - (self.__physical_range / 100))

        return minimal

    async def get_ki_min(self):
        """
        Return the minimal value of the ki damage range

        --

        :return: `None`
        """

        minimal = self.ki * (1 - (self.__ki_range / 100))

        return minimal


class CharacterCritical:

    def __init__(self):
        # Public
        self.chance = 0
        self.bonus = 0


class CharacterDefense:

    def __init__(self):
        # Public
        self.fixed = 0
        self.floating = 0
