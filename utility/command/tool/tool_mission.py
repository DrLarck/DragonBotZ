"""Mission feature tools

--

@author DrLarck

@update 07/08/20 by DrLarck"""

import asyncio

# util
from utility.entity.mission import MissionGetter
from utility.graphic.embed import CustomEmbed


class ToolMission:

    def __init__(self, client, context):
        self.client  = client
        self.context = context

        self.__databse          = self.client.database
        self.__data             = None
        self.__display_per_page = 5
        self.__total_page       = 0
        self.__getter           = MissionGetter()
    
    async def mission_manager(self):
        """Manage the missions displaying

        --

        @return None"""

        # Fill the data
        if self.__data is None:
            self.__data = await self.__getter.get_all_missions()
        
        if len(self.__data) > 0:
            # Get the total number of pages
            self.__total_page = int(
                            ((len(self.__data) - 1) / self.__display_per_page) + 1
            )

            # Display and manages the missions display 
            stop    = False
            page_id = 1

            while not stop:
                # Get the page
                page = await self.get_mission_page(1)

                # Display the page
                current_display = await self.context.send(embed=page)
                break

        return
    
    async def get_mission_page(self, page):
        """Return the mission page

        @param int page

        --

        @return object discord.Embed"""

        mission_page = await CustomEmbed().setup(
            self.client, title="Available missions",
            description=f"Page {page}/{self.__total_page}"
        )

        start = (page - 1) * self.__display_per_page
        end   = page * self.__display_per_page

        if end > len(self.__data):
            end = len(self.__data)

        mission = ""

        for i in range(start, end):
            await asyncio.sleep(0)

            current = self.__data[i]

            # Get the difficulty display
            difficulty = ""

            for j in range(current.difficulty):
                await asyncio.sleep(0)

                difficulty += ":star:"

            mission += f"`#{current.reference}`. {current.name} {difficulty}\n"
        
        mission_page.add_field(
            name="Missions : ",
            value=mission,
            inline=False
        )

        return mission_page
