"""Trade utility

--

@author DrLarck

@update 13/09/20 by DrLarck"""

import asyncio

# utility
from utility.interactive.button import Button
from utility.interactive.message import MessageInput
from utility.graphic.embed import CustomEmbed
from utility.graphic.icon import GameIcon
from utility.entity.character import CharacterGetter

# tool
from utility.command.tool.tool_shop import ToolShop

class ToolTrade:

    def __init__(self, client):
        self.client   = client
        self.database = self.client.database
        self.cache    = TradeGetter()

        self.short_character = ["character", "char"]
        self.short_zenis     = ["zenis", "zeni", 'z']

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
            # Add the trade to the cache
            await self.trade.add_to_cache(player_a, player_b)

            # Store the propositions
            players_propositions = []
            for player in players:
                await asyncio.sleep(0)

                # Get the player proposition
                await context.send(
                    f"""<@{player.id}> Enter your proposition of type : `<objectType> <objectValue>`\n
Each proposition must be separated from the others by a **whitespace**
*Example :* `character aaa0 zenis 52 character baaa0 zenis 1`"""
                )
                proposition = await self.get_player_proposition(context, player)

                # If the proposition is not empty
                if proposition is not None and len(proposition) > 0:
                    # Store the proposition
                    players_propositions.append(proposition)

                else:
                    await context.send(
                        f"<@{player.id}> Your proposition is empty, aborting"
                    )

                    return

            # Proceed to the trade
            # if both players have proposed
            if len(players_propositions) == 2:
                # Ask for validation
                validation_set = ["✅", "❌"]

                # Get the propositions display
                player_a_proposition = await self.get_proposition_display(
                    players_propositions[0]
                )

                player_b_proposition = await self.get_proposition_display(
                    players_propositions[1]
                )

                # Setup the embed
                embed.add_field(
                    name=f"{player_a.name}'s proposition",
                    value=player_a_proposition,
                    inline=False
                )

                embed.add_field(
                    name=f"{player_b.name}'s proposition",
                    value=player_b_proposition,
                    inline=False
                )

                # Display the proposition
                proposition_display = await context.send(embed=embed)

                # Check if the player a validates
                player_a_validation = await context.send(
                    f"<@{player_a.id}> Please confirm or decline the trade"
                )

                # Check the button input
                player_a_validated = await self.validation_check(
                    player_a, player_a_validation
                )

                # If the player a has validated, proceed for player b
                if player_a_validated:
                    # Re send the trade display
                    await proposition_display.delete()

                    re_proposition_display = await context.send(embed=embed)

                    # Check if the player b validates
                    player_b_validation = await context.send(
                        f"<@{player_b.id}> Please confirm or decline the trade"
                    )

                    # Check the button input
                    player_b_validated = await self.validation_check(
                        player_b, player_b_validation
                    )

                    # If the player b has validated, proceed the trade
                    if player_b_validated:
                        success = await self.proceed_trade(
                            context, players_propositions, player_a, player_b
                        )

                        # Delete proposition
                        await re_proposition_display.delete()

                        if success:
                            await context.send(
                                f"{validation_set[0]} <@{player_a.id}> <@{player_b.id}> Success !"
                            )

                        else:
                            await context.send(
                                f"{validation_set[1]} <@{player_a.id}> <@{player_b.id}> Failure !"
                            )

                    # Player b has declined
                    else:
                        # Delete proposition
                        await re_proposition_display.delete()

                        await context.send(
                            f":x: {player_b.name} has declined the trade"
                        )

                # Player a has declined
                else:
                    # Delete proposition
                    await re_proposition_display.delete()

                    await context.send(
                        f":x: {player_a.name} has declined the trade"
                    )

                    return

        else:
            await context.send(
                f":x: Trade between {player_a.name} and {player_b.name} declined"
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
            player_input = player_input.content

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
                value  = None

                # Avoid out of range error
                if i+1 <= len(player_input)-1:
                    value  = player_input[i+1]

                if value is not None:
                    # Generate current dict
                    current = {
                        "object":object,
                        "value":value
                    }

                else:
                    return None

                # Check the characters
                if current["object"].lower() in self.short_character:
                    # Check if the player owns the character
                    owns = await player.item.has_character(
                        current["value"]
                    )

                    # If the player owns the character, add it to the
                    # proposition
                    if owns:
                        proposition.append(current)

                    else:
                        char   = current["value"]
                        error += f"- You do not own the character `{char}`\n"

                # Check if it's zenis
                elif current["object"].lower() in self.short_zenis:
                    # Convert the current value to int
                    value = int(current["value"])

                    # Check if the player has enough funds
                    player_zenis = await player.resource.get_zeni()

                    # If the value is not negative
                    if value > 0:
                        # If the player has enough zenis
                        if(player_zenis >= value
                        and player_zenis >= total_zenis):
                            # Update the value
                            total_zenis += value
                            proposition.append(current)

                        else:
                            error += f"- You do not have {z} **{value:,}**\n"
                    # Negative value
                    else:
                        error += "- You provided a negative value"

        # No input provided
        else:
            return

        # Send error message
        if error != "":
            await context.send(
                f"<@{player.id}> Your proposition contains errors :\n{error}"
            )

        return proposition

    async def get_proposition_display(self, proposition):
        """Manage the proposition display

        @param list of dict proposition

        --

        @return str"""

        display = ""
        icon    = GameIcon()

        for element in proposition:
            await asyncio.sleep(0)

            # If the element is a character, display the character name
            # level, and rarity
            if element["object"].lower() in self.short_character:
                getter       = CharacterGetter()
                character_id = element["value"]

                char = await getter.get_from_unique(
                    self.client, self.client.database, character_id
                )

                if char is not None:
                    display += f"{char.rarity.icon} **{char.name}** {char.type.icon} - lv.{char.level:,}\n"

            # If the element is zenis
            elif element["object"].lower() in self.short_zenis:
                amount = int(element["value"])
                display += f"{icon.zeni} **{amount:,}**"

        return display

    async def proceed_trade(self, context, propositions, player_a, player_b):
        """Proceed to the trade, the items in proposition[0] go to
        player_b and the ones in proposition[1] go to player_a

        @param discord.ext.commands.Context

        @param list of dict propositions

        @param Player player_a

        @param player_b

        --

        @return bool"""

        success = True
        players = [player_a, player_b]
        shop    = ToolShop(self.client, context)

        for i in range(len(propositions)):
            await asyncio.sleep(0)

            # Define trader and payee
            trader              = players[i]
            current_proposition = propositions[i]

            if i == 0:
                payee = players[1]

            else:
                payee = players[0]

            # Start proposition
            for element in current_proposition:
                await asyncio.sleep(0)

                # If the element is a character
                if element["object"].lower() in self.short_character:
                    character_id = element["value"]

                    # Remove the character from the shop
                    await shop.remove_character(character_id)

                    # Remove the character from the player's team
                    slot = await trader.combat.get_fighter_slot_by_id(
                        character_id
                    )

                    # If the player has the character in his team
                    if slot is not None:
                        await trader.combat.remove_character(slot)

                    # Update character's owner id
                    await self.database.execute(
                        """
                        UPDATE character_unique
                        SET character_owner_id = $1, character_owner_name = $2
                        WHERE character_unique_id = $3;
                        """, [payee.id, payee.name, character_id]
                    )

                # If the element is zenis
                elif element["object"].lower() in self.short_zenis:
                    zenis = int(element["value"])
                    trader_zenis = await trader.resource.get_zeni()

                    # Send the zenis to the payee
                    if trader_zenis > 0:
                        await trader.resource.remove_zeni(zenis)
                        await payee.resource.add_zeni(zenis)

        return success


class TradeGetter:

    __cache = []

    async def add_to_cache(self, player_a, player_b):
        """Add a trade instance to the cache, the instance is represented by
        a dict of the 2 discord ids

        @param Player player_a, player_b

        --

        @return None"""

        trade = {
            "player_a": player_a.id,
            "player_b": player_b.id
        }

        self.__cache.append(trade)

        return

    async def remove_trade(self, discord_id):
        """Remove the trade dict which contains the discord id

        @param int discord_id

        --

        @return bool"""

        success = False

        for trade in self.__cache:
            await asyncio.sleep(0)

            # Convert the trade data into a list of id
            data = [trade["player_a"], trade["player_b"]]

            # Check if the discord id is in
            # if the id is in the data while
            # remove the trade dict
            if discord_id in data:
                self.__cache.remove(trade)
                success = True
                break

        return success
