"""
Banner object

--

Author : DrLarck

Last update : 27/01/21 by DrLarck
"""

import asyncio
import random


# util
from utility.entity.character import CharacterGetter
from utility.entity.config_parser import ConfigParser

# tool
from utility.global_tool import GlobalTool


class Banner:

    def __init__(self):
        # Public
        self.name = ""
        self.image = ""
        self.characters = []
        self.sorted = False
        self.multi = 10

        # Private
        self.__lr = []
        self.__ur = []
        self.__ssr = []
        self.__sr = []
        self.__r = []
        self.__n = []

        # Droprate as %
        self.__lr_droprate = 0.07
        self.__ur_droprate = 3
        self.__ssr_droprate = 15
        self.__sr_droprate = 33
        self.__r_droprate = 50
        self.__n_droprate = 100

        # tool
        self.__global_tool = GlobalTool()

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

    async def summon(self):
        """
        Summon a random character

        --

        :return: `Character` or `None` in case of problem
        """

        # Init
        roll = random.uniform(0, 100)

        # Get a character according to the player's roll right above
        # Check if the list is not empty
        if len(self.__lr) > 0 and roll <= self.__lr_droprate:
            # If the player get a LR character
            # Get a random LR character form the LR list
            character = random.choice(self.__lr)

            return character

        elif len(self.__ur) > 0 and roll <= self.__ur_droprate:
            character = random.choice(self.__ur)

            return character

        elif len(self.__ssr) > 0 and roll <= self.__ssr_droprate:
            character = random.choice(self.__ssr)

            return character

        elif len(self.__sr) > 0 and roll <= self.__sr_droprate:
            character = random.choice(self.__sr)

            return character

        elif len(self.__r) > 0 and roll <= self.__r_droprate:
            character = random.choice(self.__r)

            return character

        elif len(self.__n) > 0 and roll <= self.__n_droprate:
            character = random.choice(self.__n)

            return character

        return

    async def multi_summon(self):
        """
        Proceed to a multi summon

        --

        :return: `list` of `Character`
        """

        # Init
        characters = []

        for i in range(self.multi):
            await asyncio.sleep(0)

            summoned = await self.summon()

            if summoned is not None:
                characters.append(summoned)

            else:
                i -= 1

        return characters

    async def generate(self, client, name="",
                       image="", characters=""):
        """
        Generate a banner object

        :param client: discord.ext.commands.Bot
        :param name: (`str`)
        :param image: (`str`) Valid url
        :param characters: (`str`)

        --

        :return: `Banner`
        """

        # Init
        getter = CharacterGetter()

        # Set the attributes
        self.name = name
        self.image = image
        self.characters = characters

        # Get the character instances
        self.characters = self.characters.split()

        # Init the new character list
        new_character_list = []

        # The character are stored as reference id in the characters[] attribute
        for reference in self.characters:
            await asyncio.sleep(0)

            # Convert the str reference to int
            reference = int(reference)

            character = await getter.get_reference_character(reference, client)

            # Add the character into the list
            new_character_list.append(character)

        # Replace the old character list by the new one
        self.characters = new_character_list

        # Sort the banner
        await self.sort()

        return self

    async def set_unique_id(self, client):
        """
        Generate an unique id for the characters that have 'NONE' as unique id

        --

        :return: `None`
        """

        # Get the characters that have 'NONE' as unique id
        characters = await client.database.fetch_row("""
                                               SELECT reference 
                                               FROM character_unique
                                               WHERE character_unique_id is NULL;
                                               """)

        # Generate a unique id for each of them
        for character in characters:
            await asyncio.sleep(0)

            # Get the unique character's reference
            reference = character[0]
            unique_id = await self.__global_tool.generate_unique_id(reference)

            # Update the character's unique id
            await client.database.execute("""
                                         UPDATE character_unique
                                         SET character_unique_id = $1
                                         WHERE reference = $2;
                                         """, [unique_id, reference])

        return


class BannerGetter:

    # Private
    __cache = []
    __cache_ok = False
    __current_banner = 1

    # Public
    async def set_cache(self, client):
        """
        Set the banner cache

        --

        :return: `None`
        """

        if self.__cache_ok is False:
            data = await client.database.fetch_row("""
                                                   SELECT banner_name, banner_image, banner_content 
                                                   FROM banner
                                                   ORDER BY reference;
                                                   """)

            if len(data) > 0:
                for banner in data:
                    await asyncio.sleep(0)

                    # Generate the banner object
                    banner_ = Banner()

                    await banner_.generate(client, name=banner[0], image=banner[1], characters=banner[2])

                    self.__cache.append(banner_)

                self.__cache_ok = True

                print("Banner Cache : DONE")

        else:
            print("Banner Cache : The cache has already been filled.")

        return

    async def get_banner(self, reference):
        """
        Return a banner object from the cache

        :param reference: (`int`)

        --

        :return: `Banner` or `None` if not found
        """

        # Get the banner object from the cache
        if reference > 0 and reference - 1 < len(self.__cache):
            return self.__cache[reference - 1]

        else:
            print(f"Banner {reference} not found.")
            return None

    async def get_current_banner(self):
        """
        Return the last banner out

        --

        :return: `Banner`
        """

        self.__current_banner = await ConfigParser().get_config_for("banner current")
        return self.__cache[self.__current_banner - 1]
