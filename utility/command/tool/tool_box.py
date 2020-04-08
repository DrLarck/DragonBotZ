"""
Box command tools

--

Author : DrLarck

Last update : 08/04/20 by DrLarck
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
    async def box_manager(self, player, rarity=None, unique_reference=None):
        """
        Manage the box displaying

        :param rarity: (`int`)
        :param player: (`Player`)
        :param unique_reference: (`int`)

        --

        :return: `None`
        """

        # Init
        unique = False

        if self.__data is None:
            # Adapt the data
            # The player asked for a rarity box
            if rarity is not None:
                # Get all the distinct characters from the database
                # But by rarity
                self.__data = await self.__database.fetch_row("""
                                                              SELECT DISTINCT character_reference
                                                              FROM character_unique
                                                              WHERE character_owner_id = $1 AND character_rarity = $2
                                                              ORDER BY character_reference;                                                              
                                                              """, [player.id, rarity])

            # The player asked for a unique box
            elif unique_reference is not None:
                # Setup the data
                self.__data = await self.__database.fetch_row("""
                                                              SELECT character_unique_id, character_level
                                                              FROM character_unique
                                                              WHERE character_reference = $1 AND character_owner_id = $2
                                                              ORDER BY character_level DESC;
                                                              """, [unique_reference, player.id])

                unique = True

            # If the player asked for a normal box
            else:
                # Get all the distinct characters from the database
                self.__data = await self.__database.fetch_row("""
                                                              SELECT DISTINCT character_reference, character_rarity
                                                              FROM character_unique
                                                              WHERE character_owner_id = $1
                                                              ORDER BY character_rarity, character_reference;
                                                              """, [player.id])

            # If this is not a unique box call
            if not unique:
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
                                   ((len(self.__data) - 1) / self.__display_per_page) + 1
                                   )

            # Display and manage the box behaviour
            stop = False
            page_id = 1

            while not stop:
                # Display the box page from the page 1
                # Normal box
                if not unique:
                    box_page = await self.get_box(player, page_id)

                # Unique box
                else:
                    box_page = await self.get_unique_box(player, unique_reference, page_id)

                current_page = await self.context.send(embed=box_page)

                # Add buttons to the current page
                button = Button(self.client, current_page)
                box_button = await self.get_buttons(page_id)

                await button.add(box_button)

                # Get the pressed button
                pressed = await button.get_pressed(box_button, player)

                # If a button has been pressed
                if pressed is not None:
                    # Close the box
                    if pressed == '❌':
                        await current_page.delete()
                        break

                    # Go back to the first page
                    elif pressed == '⏮':
                        page_id = 1

                    # Go to the previous page
                    elif pressed == '◀':
                        page_id -= 1

                    # Go to the next page
                    elif pressed == '▶':
                        page_id += 1

                    # Go to the last page
                    elif pressed == '⏭':
                        page_id = self.__total_page

                    # Delete the current page to open a new one
                    await current_page.delete()

                # No button has been pressed
                else:
                    break

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

        # Avoid the out of range error
        if end > len(self.__data):
            end = len(self.__data)

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
            characters += f"`#{character.id}` **{character.name}** {character.rarity.icon} x{amount}\n"

        box_page.add_field(name="Characters",
                           value=characters,
                           inline=False)

        return box_page

    async def get_unique_box(self, player, reference, page):
        """
        Get the unique box page embed

        :param player: (`Player`)
        :param reference: (`int`)
        :param page: (`int`)

        --

        :return: `discord.Embed`
        """

        # Init
        box_page = await CustomEmbed().setup(self.client,
                                             title=f"{player.name}'s box",
                                             description=f"Page {page}/{self.__total_page}",
                                             thumbnail_url=player.avatar)

        reference = await self.__getter.get_reference_character(reference)

        # Display the characters
        # Get the first character to display
        # For example, if you are at page 1
        # The first character's index would be 0, and the last one 4, it would display 5 characters
        # according to the display_per_page attribute which is editable
        # If you are at the page 2, the first character index to display would be 5 and the last one 9
        # and so on ...
        start = (page - 1) * self.__display_per_page

        end = page * self.__display_per_page

        # Avoid the out of range error
        if end > len(self.__data):
            end = len(self.__data)

        # Add characters to the embed
        characters = ""

        for i in range(start, end):
            await asyncio.sleep(0)

            # Get the unique id
            unique_id = self.__data[i][0]
            character_level = self.__data[i][1]

            # Display the character
            characters += f"`#{unique_id}` **{reference.name}** {reference.rarity.icon} - lv.{character_level}\n"

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
