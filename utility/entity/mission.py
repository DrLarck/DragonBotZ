"""Mission object

--

@author DrLarck

@update 25/12/20 by DrLarck"""

import asyncio

# util
from utility.entity.character import CharacterGetter, CharacterExperience
from utility.entity.capsule import Capsule
from utility.graphic.icon import GameIcon
from utility.global_tool import GlobalTool


class Mission:

    def __init__(self, client):
        self.client      = client
        self.global_tool = GlobalTool()

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
    
    async def send_rewards(self, context, player):
        """Send the mission rewards to the player

        @param discord.ext.commands.Context context

        @param Player player

        --

        @return str"""

        rewards = ""
        premium_bonus = await self.global_tool.get_player_premium_resource_bonus(player)
        character_exp = CharacterExperience(self.client)
        icon = GameIcon()

        # Reducing the reward according to the player's team level
        average_level    = await player.combat.get_average_team_level()
        reward_reduction = 1  # If it reaches 0, the player doesn't get anything

        # Every 5 level gap, reduce the rewards by 25 % (reward_reduction - 0.25)
        gap = average_level - self.opponent_lvl

        if gap > 0:
            # Reduce the rewards by 25 % every 5 lvl gap
            reward_reduction -= 0.25 * int(gap / 5)

            if reward_reduction < 0:
                reward_reduction = 0
        
        # Update rewards
        self.experience  = int((self.experience * reward_reduction) * premium_bonus)
        self.zenis       = int((self.zenis * reward_reduction) * premium_bonus)
        self.dragonstone = int((self.dragonstone * reward_reduction) * premium_bonus)
        await player.experience.add_power(int(5 * reward_reduction))

        if reward_reduction == 0:
            self.capsule = None
        
        # Add xp to the player's characters
        if self.experience is not None:
            rewards += f"**{self.experience:,}**xp | "

            player_team = player.combat.unique_id_team
            for character in player_team:
                await asyncio.sleep(0)

                await character_exp.add_experience(character, self.experience)
        
        if self.dragonstone is not None:
            rewards += f"**{self.dragonstone:,}** {icon.dragonstone} | "

            await player.resource.add_dragonstone(self.dragonstone)

        if self.zenis is not None:
            rewards += f"**{self.zenis:,}** {icon.zeni} | "

            await player.resource.add_zeni(self.zenis)

        if self.capsule is not None:
            capsule = Capsule(context, self.client, player)
            capsule = await capsule.get_capsule_by_reference(self.capsule)

            rewards += f"**{capsule.name}** {capsule.icon}"

            await player.item.add_capsule(self.capsule)

        return rewards


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

            mission_obj = Mission(client)

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

                enemy = int(enemy)
                new_opponent = await char_getter.get_reference_character(
                    enemy, client, level=opponent_lvl
                )

                opponent_list.append(new_opponent)
            
            mission_obj.opponent = opponent_list
            mission_obj.opponent_lvl = opponent_lvl

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
        reference = int(reference)
        reference -= 1

        if reference < 0:
            reference = 0

        elif reference > len(self.__cache):
            return
        
        # Get the mission
        mission = self.__cache[reference]

        return mission
    
    async def get_all_missions(self):
        """Return the mission cache

        --

        @return Mission list"""

        return self.__cache
