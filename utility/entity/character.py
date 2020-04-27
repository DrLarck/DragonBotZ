"""
Character object

--

Author : Drlarck

Last update : 27/04/20 by DrLarck
"""

import asyncio

# util
from utility.graphic.embed import CustomEmbed
from utility.graphic.icon import GameIcon
from utility.graphic.color import GameColor


class Character:

    def __init__(self, client):
        # Public
        self.client = client

        self.name = ""
        self.id = 0
        self.unique_id = ""
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

        # Items
        self.training_item = CharacterTrainingItem(self)

        # Private
        self.__embed = CustomEmbed()

    # Public method
    async def generate(self, name="", char_id=0, level=1,
                       card="", thumbnail="",
                       type_value=0, rarity_value=0, health=0,
                       ki=100, physical=0, ki_power=0,
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

        self.ki.maximum = ki

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
        self.rarity.icon = await GameIcon().get_rarity_icon(self.rarity.value)
        self.type.icon = await GameIcon().get_type_icon(self.type.value)

        # Return the character
        return self

    async def get_display_card(self, client):
        """
        Generate a display card of this character

        :param client: (`discord.ext.commands.Bot`)

        --

        :return: `discord.Embed`
        """

        # Init
        color = await GameColor().get_rarity_color(self.rarity.value)
        embed = await self.__embed.setup(client, color=color)

        # Info
        info = f"""
__Name__ : **{self.name}**{self.type.icon}
__Reference__ : `#{self.id}`
__Rarity__ : {self.rarity.icon}
__Level__ : **{self.level}**
        """

        health = f"**{self.health.maximum:,}** :hearts:"
        ki = f"**{self.ki.maximum:,}** :fire:"

        damage = [await self.damage.get_physical_min(), self.damage.physical]
        damage_ = f"**{damage[0]:,}** - **{damage[1]:,}** :crossed_swords:"

        embed.add_field(name="Info :", value=info, inline=False)
        embed.add_field(name="Health :", value=health, inline=False)
        embed.add_field(name="Damage :", value=damage_, inline=False)
        embed.add_field(name="Ki :", value=ki, inline=False)

        embed.set_image(url=self.image.card)

        return embed

    async def init(self):
        """
        Init the character for combat purpose.

        --

        :return: `None`
        """

        return


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

        return int(minimal)

    async def get_ki_min(self):
        """
        Return the minimal value of the ki damage range

        --

        :return: `None`
        """

        minimal = self.ki * (1 - (self.__ki_range / 100))

        return int(minimal)


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


class CharacterTrainingItem:

    def __init__(self, character):
        """
        :param character: (`Character`)
        """

        # Public
        self.character = character
        self.equipped = []

        # Private
        self.__database = self.character.client.database

    # Private
    async def __get_equipped(self):
        """
        Get the equipped training items

        --

        :return: `None`
        """

        # Get the equipped items' unique id
        unique_items = await self.__database.fetch_value("""
                                                         SELECT training_item
                                                         FROM character_unique
                                                         WHERE character_unique_id = $1;
                                                         """, [self.character.unique_id])

        # Get the list of items
        unique_items = unique_items.split()

        # Set the equipped list
        self.equipped = unique_items

        return

    # Public
    async def apply_effect(self):
        """
        Apply the equipped items effects on the character

        --

        :return: `None`
        """

        # Apply the effect of each items
        for item in self.equipped:
            await asyncio.sleep(0)

            await item.apply_effect(self)

        return


class CharacterGetter:

    # Private
    __cache = []
    __cache_ok = False  # Indicates if the cache has already been filled

    # Public
    async def set_cache(self, client):
        """
        Set the character cache

        --

        :return: `None`
        """

        if self.__cache_ok is False:
            data = await client.database.fetch_row("""
                                                 SELECT *
                                                 FROM character_reference
                                                 ORDER BY reference;
                                                 """)

            if len(data) > 0:
                # Storing each character in the cache as Character objects
                for character in data:
                    await asyncio.sleep(0)

                    character_ = await Character(client).generate(char_id=character[0], name=character[1],
                                                                  type_value=character[2], rarity_value=character[3],
                                                                  card=character[4], health=character[5],
                                                                  physical=character[6])

                    self.__cache.append(character_)

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
        if reference > 0 and reference - 1 < len(self.__cache):
            return self.__cache[reference - 1]

        else:
            print(f"Character {reference} not found.")
            return None

    async def get_from_unique(self, database, unique_id):
        """
        Get a Character object from a unique id

        :param database: (`Database`)

        :param unique_id: (`str`)

        --

        :return: `Character` or `None` if not found
        """

        character_row = await database.fetch_row("""
                                                 SELECT *
                                                 FROM character_unique
                                                 WHERE character_unique_id = $1;
                                                 """, [unique_id])
        character_row = character_row[0]

        if character_row is not None:
            # Get the character object according to the character's reference
            character = await self.get_reference_character(character_row[1])

            # Setup the character object
            character.level = 6

            await character.init()

            return character

        return
