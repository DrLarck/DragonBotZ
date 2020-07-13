"""
Represents the combat object

--

Author : DrLarck

Last update : 13/07/20 by DrLarck
"""

import random
import asyncio

# util
from utility.interactive.button import Button


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

        # Move
        self.move_a = Move(self.client, self.context, self.player_a)
        self.move_b = Move(self.client, self.context, self.player_b)

        # Private
        self.__combat_tool = CombatTool(self)

    # Public
    async def run(self):
        """
        Run the combat

        --

        :return: `Player` as winner
        """

        # Set the play order
        await self.__combat_tool.define_play_order()

        # Set the teams
        await self.__combat_tool.init_teams()

        # Start combat
        turn = 1     # Start at turn 1
        end = False  # Set the variable to True to end the fight

        while not end:
            await asyncio.sleep(0)

            # Run the turn of each player
            players = [0, 1]  # Player index

            # Run the turn of each player according to the player's index
            # stored in the players variable
            for player in players:
                await asyncio.sleep(0)

                # Run the player's turn
                await self.run_turn(player)

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
        player_team = await self.__combat_tool.get_player_team_by_index(player_index)

        # Run the turn of each character
        for character in player_team:
            await asyncio.sleep(0)

            playable = await character.is_playable()

            if playable:
                # Get the move object
                move = await self.__combat_tool.get_move_by_index(player_index)

                # Get character card display
                card = await character.get_combat_card(self.client, player_index)
                await self.context.send(embed=card)

                # Get the player's move
                await move.get_move(character)

        return


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
            self.combat.player_a = self.combat.player_b
            self.combat.player_b = self.combat.player_a

        # else doesn't change anything

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


class Move:

    def __init__(self, client, context, player):
        """
        :param player: (`Player`)
        """

        # Public
        self.client = client
        self.context = context
        self.player = player

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

        :return: `int` or `None` (if the player fleed or didn't react)
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
        count = 0  # Count for the emote

        for ability in character.ability:
            await asyncio.sleep(0)

            display += f"{action[count]} - {ability.icon}**{ability.name}**\n"

            # Pass the to the next emote
            count += 1

        # Send the message
        message = await self.context.send(display)

        # Define the button manager
        button_manager = Button(self.client, message)

        # Get the reactions to add
        reactions = []

        # Add the necessary buttons
        for i in range(count):
            await asyncio.sleep(0)

            reactions.append(action[i])

        # Add all the secondary actions
        reactions += action_second

        # Add the buttons to the message
        await button_manager.add(reactions)

        # Get the player's action
        pressed = await button_manager.get_pressed(reactions, self.player)

        # If the pressed button is the flee button
        # return flee
        if pressed == action_second[0]:
            return None

        if pressed is not None:
            # Look for the index of the pressed button in the list
            index = 0
            for button in reactions:
                await asyncio.sleep(0)

                if pressed == button:
                    pressed = index
                    break

                else:
                    index += 1

        return pressed
