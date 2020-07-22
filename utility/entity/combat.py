"""
Represents the combat object

--

Author : DrLarck

Last update : 22/07/20 by DrLarck
"""

import random
import asyncio

# util
from utility.interactive.button import Button
from utility.graphic.embed import CustomEmbed
from utility.graphic.color import GameColor


class Combat:

    def __init__(self, client, context, player_a, player_b):
        """
        :param client: (`discord.ext.commands.Bot`)

        :param context: (`discord.ext.commands.Context`)

        :param player_a: (`Player` or `CPU`)

        :param player_b: (`Player` or `CPU`)
        """

        # Public
        self.client = client
        self.context = context

        # Player
        self.player_a, self.player_b = player_a, player_b
        self.team_a, self.team_b = [], []

        # Graphic
        self.color = GameColor()

        # Move
        self.move_a = Move(self.client, self.context, self.player_a, self.color.player_a)
        self.move_b = Move(self.client, self.context, self.player_b, self.color.player_b)

        # Private
        self.__combat_tool  = CombatTool(self)
        self.__combat_cache = CombatGetter()

    # Public
    async def run(self):
        """
        Run the combat

        --

        :return: `Player` as winner
        """

        # Add this combat in the cache
        await self.__combat_cache.add_combat_instance(self)

        # Set the play order
        await self.__combat_tool.define_play_order()

        # Set the teams
        await self.__combat_tool.init_teams()

        # Start combat
        turn   = 1     # Start at turn 1
        end    = False  # Set the variable to True to end the fight
        winner = None

        while not end:
            await asyncio.sleep(0)

            # Show players
            if turn == 1:
                message_intro = f"{self.player_a.circle}**{self.player_a.name}** VS {self.player_b.circle}**{self.player_b.name}**"
                await self.context.send(message_intro)

            # Send the turn id
            await self.context.send(f"📣 ROUND {turn} !")

            # Run the turn of each player
            players = [0, 1]  # Player index

            # Run the turn of each player according to the player's index
            # stored in the players variable
            for player in players:
                await asyncio.sleep(0)

                # Run the player's turn
                combat_status = await self.run_turn(player)

                # If the run_turn method returns NoneType,
                # the combat ends
                if combat_status is None:
                    end = True

                    # Flee message
                    player_ = await self.__combat_tool.get_player_by_index(player)
                    player_name   = player_.name
                    player_circle = player_.circle

                    end_message = f"{player_circle} {player_name} has fled the combat 🏃‍♂️"

                    await self.context.send(end_message)

                    # Get the winner
                    winner = await self.__combat_tool.get_player_by_index_reverse(player)
                    
                    # Delete the combat instance
                    await self.__combat_cache.remove_combat_instance(self.player_a)

                    # Return the player who won 
                    return winner

                # Check if one of the team is defeated
                winner_id = await self.__combat_tool.check_alive_team()

                # If draw, return none winner
                if winner_id == 0:
                    await self.__combat_cache.remove_combat_instance(self.player_a)
                    return None
                
                # If player A win
                elif winner_id == 1:
                    await self.__combat_cache.remove_combat_instance(self.player_a)
                    winner = self.player_a
                    return winner
                
                # If player B win
                elif winner_id == 2:
                    await self.__combat_cache.remove_combat_instance(self.player_a)
                    winner = self.player_b
                    return winner
                
                # If both team are alive
                elif winner_id is None:
                    pass

            # End of the turn
            turn += 1
        
        return

    async def run_turn(self, player_index):
        """
        Run the player's turn

        :param player_index: (`int`)

        --

        :return: `None`
        """

        # Init
        player      = await self.__combat_tool.get_player_by_index(player_index) 
        player_team = await self.__combat_tool.get_player_team_by_index(player_index)
        enemy_team  = await self.__combat_tool.get_enemy_team_by_index(player_index)

        embed = await CustomEmbed().setup(self.client, title=f"{player.circle}{player.name}'s turn",
                                          thumbnail_url=player.avatar, color=player.color)

        await self.context.send(embed=embed)
        
        # Run the turn of each character
        for character in player_team:
            await asyncio.sleep(0)

            playable = await character.is_playable()

            if playable:
                # Get the move object
                move = await self.__combat_tool.get_move_by_index(player_index)
                    
                if character.npc:
                    # Special for CPU
                    move = await player.set_move(character, move)

                # The character is not an npc
                else:
                    # Get character card display
                    card = await character.get_combat_card(self.client, player_index)
                    await self.context.send(embed=card)

                    # Get the player's move
                    await move.get_move(character)

                # Check if the player decided to flee the combat
                if move.index is None:
                    return None

                # Otherwise, use the ability
                else:
                    ability = character.ability[move.index]
                    await move.use_ability(player, character, ability, player_team, enemy_team)
        
        return move.index


class CombatTool:

    def __init__(self, combat):
        """
        :param combat: (`Combat`)
        """

        # Public
        self.combat = combat

    # Public
    async def init_teams(self):
        """
        Init the players team

        :return: `None`
        """

        # Get the team for the player
        # A
        if self.combat.player_a is not None:
            self.combat.team_a = await self.combat.player_a.combat.get_team()

        # B
        if self.combat.player_b is not None:
            self.combat.team_b = await self.combat.player_b.combat.get_team()

        return

    async def get_player_by_index(self, player_index):
        """Return the player object by index

        --

        @return object Player"""


        if player_index == 0:
            return self.combat.player_a
        
        else:
            return self.combat.player_b
    
    async def get_player_by_index_reverse(self, player_index):
        """Works the same as get_player_by_index method
        but returns the other player

        --

        @return object Player"""

        if player_index == 0:
            return self.combat.player_b
        
        else:
            return self.combat.player_a

    async def get_player_team_by_index(self, player_index):
        """
        Return the player team by player index

        :param player_index: (`int`)

        --

        :return: `list` of `Character`
        """

        if player_index == 0:
            return self.combat.team_a

        else:
            return self.combat.team_b
    
    async def get_enemy_team_by_index(self, player_index):
        """Return the player's enemy team by player index

        @param player_index int

        --

        @return list of Character"""

        if player_index == 0:
            return self.combat.team_b
        else:
            return self.combat.team_a

    async def get_move_by_index(self, player_index):
        """
        Return the right move object according to the player index

        :param player_index: (`int`

        --

        :return: `Move`
        """

        if player_index == 0:
            return self.combat.move_a

        else:
            return self.combat.move_b

    async def define_play_order(self):
        """
        Redefine player_a and player_b to define a play order

        --

        :return: `None`
        """

        # Roll the first player
        roll = random.randint(0, 1)

        # If the first player to play is the player b
        if roll == 1:
            # Save a copy of the player to avoid losing it
            copy_a      = self.combat.player_a
            copy_move_a = self.combat.move_a

            self.combat.player_a        = self.combat.player_b
            self.combat.move_a          = self.combat.move_b
            self.combat.player_a.color  = self.combat.color.player_a
            self.combat.player_a.circle = self.combat.color.player_a_circle

            self.combat.player_b        = copy_a
            self.combat.move_b          = copy_move_a
            self.combat.player_b.color  = self.combat.color.player_b
            self.combat.player_b.circle = self.combat.color.player_b_circle

        # else doesn't change anything
        else:
            self.combat.player_a.color  = self.combat.color.player_a
            self.combat.player_a.circle = self.combat.color.player_a_circle

            self.combat.player_b.color  = self.combat.color.player_b
            self.combat.player_b.circle = self.combat.color.player_b_circle

        return

    async def reset_moves(self):
        """
        Reset the moves instances

        --

        :return: `None`
        """

        await self.combat.move_a.reset()
        await self.combat.move_b.reset()

        return
    
    async def check_alive_team(self):
        """Check which team is alive

        --

        @return int (0 draw, 1 player a wins, 2 player b wins) or None if 
        both team are alive"""

        # Check team a
        team_a_alive = False

        for character_a in self.combat.team_a:
            await asyncio.sleep(0)

            if character_a.health.current > 0:
                team_a_alive = True
                break
        
        # Check team b
        team_b_alive = False

        for character_b in self.combat.team_b:
            await asyncio.sleep(0)

            if character_b.health.current > 0:
                team_b_alive = True
                break
            
        # Both team alive
        if team_a_alive and team_b_alive:
            return None

        # Player a win
        elif team_a_alive and not team_b_alive:
            return 1
        
        # Player b win
        elif team_b_alive and not team_a_alive:
            return 2
        
        # Draw
        else:
            return 0


class Move:

    def __init__(self, client, context, player, color):
        """
        :param player: (`Player`)
        """

        # Public
        self.client = client
        self.context = context
        self.player = player

        self.color = color

        self.index = 0
        self.target = None

    # Public
    async def reset(self):
        """
        Reset the move's attributes

        --

        :return: `None`
        """

        self.index = 0
        self.target = None

        return

    async def get_move(self, character):
        """
        Get the player's move for his playing character

        :param character: (`Character`)

        --

        :return: `None`
        """

        # Set of buttons
        action = [
                  "🇦", "🇧", "🇨",
                  "🇩", "🇪", "🇫",
                  "🇬", "🇭", "🇮"
                  ]

        action_second = ["🏃"]

        # Message
        display = f"Please select an action among the followings for **{character.name}**{character.type.icon} :\n"

        # Add ability name to the display
        count        = 0  # Count for the emote
        usable_index = []

        for ability in character.ability:
            await asyncio.sleep(0)

            usable, reason = await ability.is_usable(character)

            if usable:
                display += f"{action[count]} - {ability.icon}**{ability.name}** : {ability.tooltip}\n"

                # Add it to the usable list
                usable_index.append(count)

            else:
                display += f"~~/ - {ability.icon}**{ability.name}** :~~ {reason}\n"
            
            # Pass the to the next emote
            count += 1

        # Send the message
        message = await self.context.send(display)

        # Define the button manager
        button_manager = Button(self.client, message)

        # Get the reactions to add
        reactions = []

        # Add the necessary buttons
        for index in usable_index:
            await asyncio.sleep(0)

            reactions.append(action[index])

        # Add all the secondary actions
        reactions += action_second

        # Add the buttons to the message
        await button_manager.add(reactions)

        # Get the player's action
        pressed = await button_manager.get_pressed(reactions, self.player)

        # If the pressed button is the flee button
        # return flee
        if pressed is None:
            self.index = None

        if pressed == action_second[0]:
            self.index = None

        if self.index is not None:
            # Look for the index of the pressed button in the list
            index = 0
            for button in reactions:
                await asyncio.sleep(0)

                if pressed == button:
                    self.index = usable_index[index]
                    break

                else:
                    index += 1

        return
    
    async def get_enemy_target(self, enemy_team):
        """Get the available enemy targets

        --

        @return list of Character"""

        targets = []

        # First, get the defenders
        defenders = []
        for enemy in enemy_team:
            await asyncio.sleep(0)

            # If the enemy is alive and defending
            if enemy.posture == 2 and enemy.health.current > 0:
                defenders.append(enemy)
        
        # If there is no defenders, append the rest
        if len(defenders) == 0:
            for enemy_ in enemy_team:
                await asyncio.sleep(0)

                if enemy_.health.current > 0:
                    targets.append(enemy_)
        
        else:
            targets = defenders

        return targets

    async def get_ally_target(self, ally_team):
        """Get the available allied targets

        --

        @return list of Character"""

        targets = []

        for ally in ally_team:
            await asyncio.sleep(0)

            if ally.health.current > 0:
                targets.append(ally)

        return targets

    async def get_target(self, entities):
        """Allow the player to choose a target
        among the past entities

        --

        @return None"""

        # Set of buttons
        action = [
                  "🇦", "🇧", "🇨",
                  "🇩", "🇪", "🇫"
                 ]

        display = "Please select a target among the followings :\n"

        # Add target name to the display
        count = 0
        for character in entities:
            await asyncio.sleep(0)

            health = character.health.current
            health_rate = int((character.health.current * 100) / character.health.maximum)
            info = f"**{character.name}**{character.type.icon} **{health:,}**:hearts: *({health_rate} %)*"

            display += f"{action[count]} - {info}\n"

            count += 1
        
        # Send the message
        message = await self.context.send(display)

        button_manager = Button(self.client, message)

        # Get the reactions to add
        reactions = []

        # Add necessary buttons
        for i in range(count):
            await asyncio.sleep(0)

            reactions.append(action[i])

        # Add the reactions under the message
        await button_manager.add(reactions)

        # Get the player's action
        pressed = await button_manager.get_pressed(reactions, self.player)

        # Get the index of the pressed button
        index = 0
        for button in reactions:
            await asyncio.sleep(0)

            if pressed == button:
                self.target = entities[index]
            
            else:
                index += 1

        return

    async def use_ability(self, player, caster, ability, ally_team, enemy_team):
        """Use the ability

        --

        @return None"""

        # Setup the ability
        if ability.need_target:
            targets = []

            # Get the allied targets
            if ability.target_ally:
                allies = await self.get_ally_target(ally_team)

                targets += allies

            # Get the enemy targets
            if ability.target_enemy:
                enemies = await self.get_enemy_target(enemy_team)

                targets += enemies

            if not caster.npc:
                await self.get_target(targets)
            
            else:
                self.target = await player.choose_target(targets)

        # If no target required, self target
        else:
            self.target = caster

        # Set the display
        embed_title = f"{caster.image.icon}{caster.name}'s action to {self.target.image.icon}{self.target.name}"
        embed = await CustomEmbed().setup(self.client, title=embed_title, thumbnail_url=caster.image.thumbnail,
                                          color=self.color)

        display = await ability.use(caster, self.target)

        embed.add_field(name=f"Action : {ability.icon}{ability.name}", value=display, inline=False)

        await self.context.send(embed=embed)

        return


class CombatGetter:

    # Store Combat objects
    __cache    = []

    async def add_combat_instance(self, instance):
        """Add an existing combat instance to the cache

        @param instance object Combat

        --

        @return None"""
        
        self.__cache.append(instance)

        return

    async def remove_combat_instance(self, player):
        """Remove the combat instance where the specified
        player is in

        @param player object Player

        --

        @return None"""

        for combat in self.__cache:
            await asyncio.sleep(0)

            if combat.player_a.id == player.id or combat.player_b.id == player.id:
                self.__cache.remove(combat)
                break

        return
    
    async def player_is_fighting(self, player):
        """Find a Combat instance where the player is

        @param player object Player

        --

        @return bool"""

        fighting = False

        for combat in self.__cache:
            await asyncio.sleep(0)

            if combat.player_a.id == player.id:
                fighting = True
                break

            elif combat.player_b.id == player.id:
                fighting = True
                break

        return fighting
