"""
On error event handler

--

Author : DrLarck

Last update : 21/03/20 by DrLarck
"""

from discord.ext import commands

# commands
from command.summon import CommandSummon


class EventOnError(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, context, error):
        """
        This is triggered when a command error occurs

        :param context: (`discord.ext.commands.Context`)
        :param error: (`Exception`)

        --

        :return: `None`
        """

        # Command not found error
        if isinstance(error, commands.CommandNotFound):
            # Ignore the exception
            pass

        # Command check failure
        if isinstance(error, commands.CheckFailure):
            # Ignore the exception
            pass

        return


def setup(client):
    client.add_cog(EventOnError(client))
