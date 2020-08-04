"""Mission object

--

@author DrLarck

@update 04/08/20 by DrLarck"""

import asyncio

from utility.entity.character import CharacterGetter


class Mission:

    def __init__(self):
        self.reference    = 0
        self.name         = ""
        self.description  = ""

        self.difficulty   = 1
        self.opponent     = []
        self.opponent_lvl = 1

        self.experience  = None
        self.zenis       = None
        self.dragonstone = None
        self.capsule     = None


class MissionGetter:

    __cache    = []

    async def get_cache_size(self):
        """Return the size of the mission cache

        --

        @return list"""

        return len(self.__cache)

    async def set_cache(self, client):
        """Set the mission cache

        @param client discord.ext.commands.Bot

        --

        @return None"""

        database = client.database

        # Retrieve the missions
        query = """
        SELECT *
        FROM mission
        ORDER BY reference;"""

        missions = await database.fetch_row(query)

        if len(missions) <= 0:
            return

        char_getter = CharacterGetter()

        for mission in missions:
            await asyncio.sleep(0)

            mission_obj = Mission()

            mission_obj.reference   = mission[0]
            mission_obj.name        = mission[1]
            mission_obj.description = mission[2] 

            mission_obj.difficulty = mission[3]

            # Get the opponents
            opponents    = mission[4]
            opponents    = opponents.split()
            opponent_lvl = mission[5] 
            
            opponent_list = []
            for enemy in opponents:
                await asyncio.sleep(0)

                new_opponent = await char_getter.get_reference_character(
                    enemy, client, level=opponent_lvl
                )

                opponent_list.append(new_opponent)
            
            mission_obj.opponent = opponent_list

            # Get the rewards
            mission_obj.experience  = mission[6]
            mission_obj.zenis       = mission[7]
            mission_obj.dragonstone = mission[8]
            mission_obj.capsule     = mission[9]

            # Add the mission object to the cache
            self.__cache.append(mission_obj)

        return

    async def get_mission(self, reference):
        """Get the mission according to the passed reference

        @param int reference

        --

        @return object Mission or None if not found"""

        mission = None

        reference -= 1

        if reference < 0:
            reference = 0

        elif reference > len(self.__cache):
            return
        
        # Get the mission
        mission = self.__cache[reference]

        return mission
