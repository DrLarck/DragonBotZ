"""
Command checker

--

Author : DrLarck

Last update : 12/03/20 by DrLarck
"""


class CommandChecker:

    # Public
    # Command checks
    async def game_ready(self, context):
        """
        Check if the game is ready

        :param context: (`discord.ext.commands.Context`)

        --

        :return: `bool`
        """

        # Init
        client = context.bot

        return client.is_ready()