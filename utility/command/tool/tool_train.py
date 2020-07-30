"""Train tool object

--

@author DrLarck

@update 30/07/20 by DrLarck"""

import asyncio
import random

# util
from utility.entity.character import CharacterGetter


class ToolTrain:

    def __init__(self, client):
        self.client = client
    
    async def generate_opponent_team(self, player):
        """Generate a fair opponent team according
        to the player's team

        @param Player player

        --

        @return Character list

        @return int list as average level"""

        opponent_team    = []
        character_getter = CharacterGetter()

        # Get the player's team
        player_team   = await player.combat.get_team()

        # Get the average player's team level
        average_level = 0

        for character in player_team:
            await asyncio.sleep(0)

            average_level += character.level
        
        average_level = int(average_level / len(player_team))

        # Set the level range
        level_range = [int(average_level * 0.75), average_level]

        # Generate the opponent team
        # every 50 levels, add a new character in the team
        opponent_number     = int(average_level / 50)
        existing_characters = await character_getter.get_cache_size()
        existing_characters -= 1

        for i in range(opponent_number):
            await asyncio.sleep(0)

            character_id = random.randint(0, existing_characters)
            character    = await character_getter.get_reference_character(character_id, self.client)

            opponent_team.append(character)

        return opponent_team, level_range
