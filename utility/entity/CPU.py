"""CPU object for combat purpose

--

@author DrLarck

@update 22/07/20 by DrLarck"""

import random
import asyncio

from utility.entity.player import Player


class CPU(Player):

    def __init__(self, context, client, user):
        Player.__init__(self, context, client, user)

        self.name = ""
        self.avatar = ""
        self.id = 0

        # Overwrite get_team
        self.combat.get_team = self.get_team

    async def set_team(self, team, level_range):
        """Set the CPU's team according to the passed
        characters as team and level range

        @param list of object Character team

        @param list of int level_range

        --

        @return None"""

        for character in team:
            await asyncio.sleep(0)

            # Randomly set the character's level
            character_level = random.randint(level_range[0], level_range[1])
            character.level = character_level

            # Set the character as npc
            character.npc = True

            # Add the character to the CPU's team
            self.combat.team.append(character)
        
        return
    
    async def set_move(self, character, move):
        """Set the move object

        @param object Character character

        @param object Move move

        --

        @return object Move"""

        usable_index = []  # Contains the id of the ability it can use

        index = 0
        for ability in character.ability:
            await asyncio.sleep(0)

            usable, reason = await ability.is_usable(character)

            if usable:
                usable_index.append(index)

            index += 1
        
        # Randomly choose 
        move.index = random.choice(usable_index)

        return move
    
    async def choose_target(self, targets):
        """Choose a target for the ability

        --

        @return object Character"""
        
        # Randomly choose the target
        target = random.choice(targets)

        return target

    # Overwrite get_team method
    async def get_team(self):
        return self.combat.team
