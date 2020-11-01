"""
Character object

--

Author : Drlarck

Last update : 1/11/20 by DrLarck
"""

import asyncio

# util
from utility.graphic.embed import CustomEmbed
from utility.graphic.icon import GameIcon
from utility.graphic.color import GameColor
from utility.entity.ability import Ability


class Character:

    def __init__(self, client):
        # Public
        self.client = client

        self.name = ""
        self.id = 0
        self.unique_id = ""
        self.level = 1

        self.npc = False  # Tells if it's a non playable character
        self.posture = 0

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

        # Abilities
        self.ability = []

        # Private
        self.__embed = CustomEmbed()

    # Public method
    async def generate(self, name="", char_id=0, level=1,
                       card="", thumbnail="",
                       type_value=0, rarity_value=0, health=0,
                       ki=100, physical=0, ki_power=0,
                       crit_chance=0, crit_bonus=0, armor_fixed=0,
                       armor_floating=0, spirit_fixed=0, spirit_floating=0,
                       ability=[]):
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
        :param ability: (`list`)

        --

        :return: `Character`
        """

        # New character instance
        new_char = Character(self.client)

        # Init all the attributes
        new_char.name = name
        new_char.id = char_id
        new_char.level = level
        # Set bonus per lvl
        level_bonus = pow(1.02, new_char.level-1)  # Default +5 % stat per level

        new_char.image.card = card
        new_char.image.thumbnail = thumbnail

        new_char.type.value = type_value
        new_char.rarity.value = rarity_value

        new_char.health.maximum = int(health * level_bonus)

        new_char.ki.maximum = ki

        new_char.damage.physical = int(physical * level_bonus)
        new_char.damage.ki = int(ki_power * level_bonus)

        new_char.critical.chance = crit_chance
        new_char.critical.bonus = crit_bonus

        new_char.armor.fixed = int(armor_fixed * level_bonus)
        new_char.armor.floating = armor_floating

        new_char.spirit.fixed = int(spirit_fixed * level_bonus)
        new_char.spirit.floating = spirit_floating

        # Get the character's abilities
        ability_ref = Ability(self.client)
        for ability_id in ability:
            await asyncio.sleep(0)

            # If the ability id is not an actual ability
            if not isinstance(ability_id, Ability):
                # Get the id as int
                ability_id = int(ability_id)

                # Get the ability instance
                ability = await ability_ref.get_ability_data(ability_id)

                # If the ability has been found, add it to the character
                if ability is not None:
                    new_char.ability.append(ability)

        # If the char has no abilities, add passed abilities as parameter
        if len(new_char.ability) == 0:
            new_char.ability = ability

        # Get the icons
        new_char.rarity.icon = await GameIcon().get_rarity_icon(new_char.rarity.value)
        new_char.type.icon = await GameIcon().get_type_icon(new_char.type.value)

        # Return the character
        return new_char

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
        """

        embed.add_field(name="Info :", value=info, inline=False)

        embed.set_image(url=self.image.card)

        return embed

    async def get_combat_card(self, client, team_index):
        """
        Return the combat format display card

        :param client: (`discord.ext.commands.Bot`)

        :param team_index: (`int`)

        --

        :return: `Embed`
        """

        # Init
        color = GameColor()

        if team_index == 0:
            color = color.player_a

        else:
            color = color.player_b

        # Thumbnail
        # If the thumbnail is not defined, use the card image
        if self.image.thumbnail == "":
            thumb = self.image.card

        # Use the defined thumbnail image
        else:
            thumb = self.image.thumbnail

        embed = await self.__embed.setup(client, color=color, thumbnail_url=thumb)

        # Setting up the character display
        display_info = f"""
__Name__ : {self.image.icon}**{self.name}**{self.type.icon}
__Level__ : {self.level:,}
__Health__ : **{self.health.current:,}**/{self.health.maximum:,} :hearts:
__Ki__ : **{self.ki.current}**/{self.ki.maximum} :fire:
"""
        # Damage
        phy_min = await self.damage.get_physical_min()
        ki_min = await self.damage.get_ki_min()

        display_damage = f"""
__Physical__ : **{phy_min:,}** - **{self.damage.physical:,}** :punch:
__Ki power__ : **{ki_min:,}** - **{self.damage.ki:,}** ☄️
"""
        # Defense
        display_defense = f"""
__Armor__ : **{self.armor.fixed:,}** | **{self.armor.floating:,} %** :shield:
__Spirit__ : **{self.spirit.fixed:,}** | **{self.spirit.floating:,} %** 🏵️
"""
        # Fields
        embed.add_field(name=f"**{self.name}** info",
                        value=display_info,
                        inline=False)

        embed.add_field(name="Damage",
                        value=display_damage,
                        inline=False)

        embed.add_field(name="Defense",
                        value=display_defense,
                        inline=False)

        return embed

    async def init(self):
        """
        Init the character for combat purpose.

        --

        :return: `None`
        """

        # Init health
        await self.health.init()

        # Init abilities
        for ability in self.ability:
            await asyncio.sleep(0)

            await ability.init(self)

        return

    async def is_playable(self):
        """
        Tells if the character is playable or not

        --

        :return: `bool`
        """

        # Init
        playable = True

        # If the character is stunned
        if self.posture == 3:
            playable = False

        # If the character is dead
        elif self.health.current <= 0:
            playable = False

        # If the character has posture a normal posture
        else:
            playable = True

        return playable


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
    async def get_cache_size(self):
        """Return the cache size

        --

        @return int"""

        return len(self.__cache)

    async def set_cache(self, client):
        """
        Set the character cache

        :param client: object discord.Bot
        :param context: object discord.ext.commands.Context

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

                    # Get the set of character's abilities
                    ability_set = character[15]
                    ability_set = ability_set.split()

                    character = await Character(client).generate(
                        char_id=character[0], name=character[1], type_value=character[2],
                        rarity_value=character[3], card=character[4], thumbnail=character[4],
                        health=character[5], ki=character[6], physical=character[7],
                        ki_power=character[8], armor_fixed=character[9], armor_floating=character[10],
                        spirit_fixed=character[11], spirit_floating=character[12],
                        ability=ability_set
                    )

                    self.__cache.append(character)

                # Cache has been filled
                self.__cache_ok = True
                print("Character Cache : DONE")

        else:  # The cache has already been filled
            print("Character Cache : The cache has already been filled.")

        return

    async def get_reference_character(self, reference, client, level=1):
        """
        Get a base character

        :param reference: (`int`)

        @param int level

        @param object discord.ext.commands.Bot client

        --

        :return: `Character` or `None`
        """

        # Get the character from the cache
        if reference > 0 and reference - 1 < len(self.__cache):
            char = self.__cache[reference - 1]

            copy = await Character(client).generate(
                char_id=char.id, level=level, name=char.name, card=char.image.card,
                thumbnail=char.image.thumbnail, type_value=char.type.value,
                rarity_value=char.rarity.value, health=char.health.maximum,
                ki=char.ki.maximum, physical=char.damage.physical, ki_power=char.damage.ki,
                armor_fixed=char.armor.fixed, armor_floating=char.armor.floating,
                spirit_fixed=char.spirit.fixed, spirit_floating=char.spirit.floating,
                ability=char.ability
            )

            await copy.init()

            return copy

        else:
            print(f"Character {reference} not found.")
            return None

    async def get_from_unique(self, client, database, unique_id):
        """
        Get a Character object from a unique id

        :param client: discord.ext.commands.Bot

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

        # If the character exists
        if len(character_row) > 0:
            character_row = character_row[0]

        # If the character doesn't exist
        else:
            return

        if character_row is not None:
            # Get the character object according to the character's reference
            character = await self.get_reference_character(character_row[1], client)

            # Create a copy of the character
            copy = await character.generate(
                name=character.name, char_id=character.id,
                level=character_row[6], card=character.image.card,
                thumbnail=character.image.thumbnail,
                type_value=character.type.value,
                rarity_value=character.rarity.value,
                health=character.health.maximum, ki=character.ki.maximum,
                physical=character.damage.physical, ki_power=character.damage.ki,
                armor_fixed=character.armor.fixed, armor_floating=character.armor.floating,
                spirit_fixed=character.spirit.fixed, spirit_floating=character.spirit.floating,
                ability=character.ability
            )

            await copy.init()

            return copy

        return


class CharacterExperience:

    def __init__(self, client):
        self.client     = client
        self.__database = self.client.database

    async def add_experience(self, unique_id, amount):
        """Add experience points to the character

        @param str unique_id

        @param int amount

        --

        @return int or None as new character level"""

        # Get the character's experience
        get_exp = """SELECT character_experience
        FROM character_unique
        WHERE character_unique_id = $1;"""

        character_exp = await self.__database.fetch_value(get_exp, [unique_id])

        # Add the amount of exp to the character experience
        character_exp += amount

        # Check if the character levels up
        # returns the updated amount of exp
        # and the nex character level if it has changed
        character_exp, new_level = await self.level_up(unique_id, character_exp)

        # Update character xp
        update_exp = """UPDATE character_unique
        SET character_experience = $1
        WHERE character_unique_id = $2;"""

        await self.__database.execute(update_exp, [character_exp, unique_id])

        return new_level

    async def level_up(self, unique_id, experience):
        """Update the character level according to its current level
        and the amount of exp that it has

        @param str unique_id

        @param int experience

        --

        @return int new amount of experience"""

        # Level up formula
        # level 1 character has to collect 100 exp points
        # to level up to the level 2
        # the amount of exp needed is increased by 10 % per level
        # formula is :
        # next_level : level -> 100 * (1.1) ^ level

        # Get the character's informations
        character_level = """SELECT character_level
        FROM character_unique
        WHERE character_unique_id = $1;"""

        level = await self.__database.fetch_value(character_level, [unique_id])
        old_level = level

        # Get the required amount of exp to reach the next level
        next_level = int(100 * pow(1.1, level))

        # Check if the character has enough exp to reach the next level
        # repeat it until the character experience is inferior to the
        # next level
        while experience >= next_level and level < 150:
            await asyncio.sleep(0)

            level += 1
            experience -= next_level

            # Get the required amount of exp to reach the next level
            next_level = int(100 * pow(1.1, level))

        # Update the character level
        update_level = """UPDATE character_unique
        SET character_level = $1
        WHERE character_unique_id = $2;"""

        await self.__database.execute(update_level, [level, unique_id])

        # Check if the character has leveled up
        new_level = None

        if level != old_level:
            new_level = level

        return experience, new_level
