"""
Command checker

--

Author : DrLarck

Last update : 20/03/20 by DrLarck
"""

from discord.channel import DMChannel

# util
from utility.entity.player import Player


class CommandChecker:

    # Public
    # Command checks
    @staticmethod
    async def game_ready(context):
        """
        Check if the game is ready

        :param context: (`discord.ext.commands.Context`)

        --

        :return: `bool`
        """

        # Init
        client = context.bot

        return client.is_ready()

    @staticmethod
    async def no_dm(context):
        """
        Avoid the player to use the command in DM channel

        :param context: (`discord.ext.commands.Context`)

        --

        :return: `bool`
        """

        # Init
        message_channel = context.message.channel

        # If the channel is a DM channel
        if isinstance(message_channel, DMChannel):
            return False  # The command will be ignored

        # Not a DM channel
        else:
            return True

    @staticmethod
    async def can_register(context):
        """
        Check if the player is registered, if he's not registered, he can process the command

        :param context: (`discord.ext.commands.Context`)

        --

        :return: `bool`
        """

        # Init
        client = context.bot
        player = Player(context, client, context.message.author)
        database = client.database

        # Check if the player is in the database
        value = await database.fetch_value(f"SELECT player_name FROM player_info WHERE player_id = {player.id};")

        # If the player is already registered
        # Send an error message telling him
        # That he is already registered
        if value is not None:
            await context.send(":x: You are already registered.")

            return False

        else:  # Allow the player to process the command if he is not registered
            return True

    @staticmethod
    async def register(context):
        """
        Check if the player is registered, if he is registered, he can process the command

        :param context: (`discord.ext.commands.Context`)

        --

        :return: `bool`
        """

        # Init
        client = context.bot
        player = Player(context, client, context.message.author)
        database = client.database

        # Check if the player is in the database
        value = await database.fetch_value(f"SELECT player_name FROM player_info WHERE player_id = {player.id};")

        # If the player is registered
        # Return true
        if value is not None:
            return True

        else:  # The player is not registered
            await context.send(":x: You are not registered, to do so, use the `d!start` command.")

            return False
