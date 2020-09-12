"""Trade utility

--

@author DrLarck

@update 12/09/20 by DrLarck"""

import asyncio

# utility
from utility.interactive.button import Button
from utility.graphic.embed import CustomEmbed


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
            for player in players:
                await asyncio.sleep(0)



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

    async def get_proposition(self, player):
        """Get the player porposition

        @param Player player

        --

        @return list of dict or None"""

        # Stores the proposed items by the player
        proposition = []

        # Check if the player has stoped the proposition
        stop = False
        while not stop:
            await asyncio.sleep(0)

            pass

        return proposition
