"""Trade utility

--

@author DrLarck

@update 12/09/20 by DrLarck"""

import asyncio

# utility
from utility.interactive.button import Button
from utility.interactive.message import MessageInput
from utility.graphic.embed import CustomEmbed
from utility.graphic.icon import GameIcon


class ToolTrade:

    def __init__(self, client):
        self.client   = client
        self.database = self.client.database

    async def trade(self, context, player_a, player_b):
        """Launches a trade between the player_a and the player_b

        @param discord.ext.commands.Context

        @param Player player_a

        @param Player player_b

        --

        @return None"""

        players = [player_a, player_b]

        # Define the embed object
        embed = await CustomEmbed().setup(
            self.client, title="Trade"
        )

        # Asks if the player_b wants to trade
        ask_trade = await context.send(
            f"<@{player_b.id}> **{player_a.name}** wants to trade with you !"
        )

        # Get the validation of the player b
        validated = await self.validation_check(player_b, ask_trade)

        # If the player b has accepted, start the trade
        if validated:
            # Store the propositions
            players_propositions = []
            for player in players:
                await asyncio.sleep(0)

                # Get the player proposition
                proposition = await self.get_player_proposition(player)

                # If the proposition is not empty
                if proposition is not None and len(proposition) > 0:
                    # Store the proposition 
                    players_propositions.append(proposition)

                else:
                    await context.send(
                        f"<@{player.id}> Your proposition is empty, aborting"
                    )

                return

        else:
            await context.send(
                f"Trade between {player_a.name} and {player_b.name} declined"
            )

        return

    async def validation_check(self, player, message):
        """Check if the player has validated

        @param Player player

        @param discord.Message message

        --

        @return bool, None in case of error"""

        button = Button(self.client, message)

        # Turns to True if the green mark is pressed
        validated = False

        # Define the emojis
        validation = ["✅", "❌"]

        # Add buttons to the message
        await button.add(validation)

        # Get which button has been pressed
        pressed = await button.get_pressed(validation, player)

        if pressed is not None:
            # Check if the pressed button is the valid mark
            if pressed == validation[0]:
                validated = True

        # None button has been pressed
        else:
            return None

        return validated

    async def get_player_proposition(self, context, player):
        """Get the player's get_proposition

        @param discord.ext.commands.Context

        @param Player player

        --

        @return list of dict or None"""

        # Stores the proposed items by the player
        proposition = []
        input       = MessageInput(self.client)
        icon        = GameIcon()

        z  = icon.zeni

        # Stores error
        error = ""

        # Checkers
        total_zenis = 0

        player_input = await input.get_input(player)

        if player_input is not None:
            # Get a list of string
            player_input = player_input.split()
            max_length   = 10
            length       = len(player_input)

            if length > max_length:
                length = max_length

            # Retrieve the input data
            # step : 2
            for i in range(0, length, 2):
                await asyncio.sleep(0)

                # Get the object data
                object = player_input[i]
                # Avoid out of range error
                if i+1 <= len(player_input)-1:
                    value  = player_input[i+1]

                # Generate current dict
                current = {
                    "object":object,
                    "value":value
                }

                # Check the characters
                if current["object"].lower() in ["character", "char"]:
                    # Check if the player owns the character
                    owns = await player.item.has_character(
                        current["value"]
                    )

                    # If the player owns the character, add it to the
                    # proposition
                    if owns:
                        porposition.append(current)

                    else:
                        char   = current["value"]
                        error += f"- You do not own the character `{char}`\n"

                # Check if it's zenis
                elif current["object"].lower() in ["zenis", 'z']:
                    # Convert the current value to int
                    value = int(current["value"])

                    # Check if the player has enough funds
                    player_zenis = await player.resource.get_zeni()

                    # If the player has enough zenis
                    if player_zenis >= value
                    and player_zenis > total_zenis:
                        # Update the value
                        total_zenis_proposed += value
                        proposition.append(current)

                    else:
                        error += f"- You do not have {z} {total_zenis:,}\n"

        # No input provided
        else:
            return

        # Send error message
        if error != "":
            await context.send(
                f"<@{player.id}> Your proposition contains errors :\n{error}"
            )

        return proposition
