"""
Command checker

--

Author : DrLarck

Last update : 13/03/20 by DrLarck
"""

from discord.channel import DMChannel


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
