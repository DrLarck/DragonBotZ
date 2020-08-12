"""Manages the shop

--

@author DrLarck

@update 12/08/20 by DrLarck"""

import asyncio
import time

# util
from utility.graphic.embed import CustomEmbed
from utility.entity.character import CharacterGetter
from utility.graphic.icon import GameIcon
from utility.interactive.button import Button
from utility.command.tool.tool_time import ToolTime


class ToolShop:

    def __init__(self, client, context):
        self.client  = client
        self.context = context

        self.__database         = self.client.database
        self.__data             = None
        self.__display_per_page = 5
        self.__total_page       = 0

    async def shop_manager(self, player, shop_type=0, character_id=None):
        """Manage the shop displaying

        @param Player player

        @param int shop_type : Character shop

        @param int character_id 

        --

        @return None"""

        # Load data according to the shop type
        if shop_type is 0:
            if character_id is None:
                # All character shop
                await self.set_data_character()

            else:
                # Specific character id
                await self.set_data_character(character_id=character_id)
        
        # If there is still no data
        if self.__data is None:
            await self.context.send(":x: None on sale characters at this reference")
            return

        elif len(self.__data) > 0:
            # Get the number of page
            self.__total_page = int(
                ((len(self.__data) - 1) / self.__display_per_page) + 1
            )

            stop    = False
            page_id = 1

            while not stop:
                await asyncio.sleep(0)

                page = await self.get_character_shop_page(page_id)

                current_page = await self.context.send(embed=page)

                button = Button(self.client, current_page)
                button_set = await self.get_buttons(page_id)

                await button.add(button_set)

                pressed = await button.get_pressed(button_set, player)

                if pressed is not None:
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
                    
                    # Delete to open a new one
                    await current_page.delete()
                
                else:
                    break
                
        return
    
    async def set_data_character(self, character_id=None):
        """Set the tool data with passed character id
        if character id is None, display all the characters
        
        All ordered by price

        --

        @return None"""

        # Retrieve data
        if character_id is not None:
            self.__data = await self.__database.fetch_row("""
                                                          SELECT * 
                                                          FROM shop_character
                                                          WHERE character_reference = $1
                                                          ORDER BY character_price;
                                                          """, [character_id])  

        else:
            self.__data = await self.__database.fetch_row("""
                                                          SELECT *
                                                          FROM shop_character
                                                          ORDER BY character_price;
                                                          """)
        
        if self.__data == []:
            self.__data = None

        return
    
    async def get_character_shop_page(self, page):
        """Get the character shop page

        @param int page

        --

        @return discord.Embed"""

        getter = CharacterGetter()
        start = (page - 1) * self.__display_per_page
        end = page * self.__display_per_page
        icon = GameIcon()

        if end > len(self.__data):
            end = len(self.__data)
        
        # Shop display
        shop = ""
        # Manage the time
        timer = ToolTime()
        time_now = time.time()

        max_time = 604800  # Lasts 1 week
        # Filter the character that have exceeded the time
        max_ending = time_now - max_time  # Remove character that have been put on sale a week ago from now

        await self.__database.execute("""
                                      DELETE
                                      FROM shop_character
                                      WHERE character_on_sale_at <= $1;
                                      """, [max_ending])

        for i in range(start, end):
            await asyncio.sleep(0)

            current = self.__data[i]
            character = await getter.get_from_unique(self.client, self.__database, current[1])
            
            # Remaining time calculation
            end_at         = current[4] + max_time
            time_remaining = await timer.convert_time(end_at - time_now)

            shop += f"`{current[1]}`. **{character.name}** lv.**{character.level}** | Price : {icon.zeni}**{current[3]:,}** | {time_remaining}"

        shop_page = await CustomEmbed().setup(
            self.client, title=f"Character shop", 
            description=f"Page {page}/{self.__total_page}"
        )

        shop_page.add_field(
            name=f"Available characters",
            value=shop,
            inline=False
        )

        return shop_page
    
    async def get_buttons(self, page):
        """Return a set of buttons to add

        @param int page

        --

        @return str list"""

        button_set = ['❌']

        if page > 1:
            button_set.append('⏮')
            button_set.append('◀')
        
        if page < self.__total_page:
            button_set.append('▶')
            button_set.append('⏭')

        return button_set
