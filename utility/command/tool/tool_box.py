"""
Box command tools

--

Author : DrLarck

Last update : 07/04/20 by DrLarck
"""

import asyncio

# util
from utility.interactive.button import Button
from utility.graphic.embed import CustomEmbed
from utility.entity.character import CharacterGetter


class ToolBox:

    def __init__(self, client, context):
        # Public
        self.client = client
        self.context = context

        # Private
        self.__database = self.client.database
        self.__data = None
        self.__display_per_page = 5
        self.__total_page = 0
        self.__getter = CharacterGetter()

    # Public
    async def box_manager(self, player):
        """
        Manage the box displaying

        :param player: (`Player`)

        --

        :return: `None`
        """

        # Init
        if self.__data is None:
            # Get all the distinct characters from the database
            self.__data = await self.__database.fetch_row("""
                                                          SELECT DISTINCT character_reference
                                                          FROM character_unique
                                                          WHERE character_owner_id = $1
                                                          ORDER BY character_reference;
                                                          """, [player.id])

            # Get the character objects
            new_data = []

            for reference in self.__data:
                await asyncio.sleep(0)

                character = await self.__getter.get_reference_character(reference[0])

                new_data.append(character)

            # Replace the data by the characters objects
            self.__data = new_data

        # If the player has at least one character
        if len(self.__data) > 0:
            # Get the total number of page
            self.__total_page = int(
                                   (len(self.__data) - 1 / self.__display_per_page) + 1
                                   )

            # Display and manage the box behaviour
            stop = False
            page_id = 1

            while not stop:
                # Display the box page from the page 1
                box_page = await self.get_box(player, page_id)

                current_page = await self.context.send(embed=box_page)

                # Add buttons to the current page

        # If the player doesn't have any character
        else:
            await self.context("You do not have any character")

        return

    async def get_box(self, player, page):
        """
        Get the box page embed

        :param player: (`Player`)
        :param page: (`int`)

        --

        :return: `discord.Embed`
        """

        # Init
        box_page = await CustomEmbed().setup(self.client,
                                             title=f"{player.name}'s box",
                                             description=f"Page {page}/{self.__total_page}",
                                             thumbnail_url=player.avatar)

        # Display the characters
        # Get the first character to display
        # For example, if you are at page 1
        # The first character's index would be 0, and the last one 4, it would display 5 characters
        # according to the display_per_page attribute which is editable
        # If you are at the page 2, the first character index to display would be 5 and the last one 9
        # and so on ...
        start = (page - 1) * self.__display_per_page

        end = page * self.__display_per_page

        # Add characters to the embed
        characters = ""

        for i in range(start, end):
            await asyncio.sleep(0)

            # Get the current character
            character = self.__data[i]

            # Get the amount of characters the player owns
            amount = await self.__database.fetch_row("""
                                                     SELECT * FROM character_unique
                                                     WHERE character_reference = $1
                                                     AND character_owner_id = $2;
                                                     """, [character.id, player.id])

            amount = len(amount)

            # Display the character
            characters += f"**{character.name}**{character.rarity.icon} x{amount}\n"

        box_page.add_field(name="Characters",
                           value=characters,
                           inline=False)

        return box_page

    async def get_buttons(self, page_id):
        """
        Get a list of buttons to add to the page

        :param page_id: (`int`)

        --

        :return: `list` of `emote`
        """

        # Init
        # By default, the ❌ emote is here
        emote = ['❌']

        # If it's not the first page
        if page_id > 1:
            emote.append('⏮')
            emote.append('◀')

        # If it's not the last page
        if page_id < self.__total_page:
            emote.append('▶')
            emote.append('⏭')

        return emote
