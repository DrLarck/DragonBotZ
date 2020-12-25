"""
On error event handler

--

Author : DrLarck

Last update : 25/12/20 by DrLarck
"""

from discord.ext import commands


class EventOnError(commands.Cog):

    def __init__(self, client):
        self.client = client

    # noinspection PyUnusedLocal
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
            await context.send("Command not found, please refer to `help`")

        # Command check failure
        if isinstance(error, commands.CheckFailure):
            await context.send("You do not fill the requirements to perform this action")

        # Command missing argument
        if isinstance(error, commands.MissingRequiredArgument):
            await context.send("Incomplete command")
        
        # Command cooldown
        if isinstance(error, commands.CommandOnCooldown):
            cd = int(error.retry_after)

            await context.send(f"⌛ You are under cooldown for this command, retry after **{cd:,}s**")
            pass

        # Print unhandled error
        else:
            print(error)

        return


def setup(client):
    client.add_cog(EventOnError(client))
