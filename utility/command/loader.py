"""
Command loader

--

Author : DrLarck

Last update : 05/04/20 by DrLarck
"""

import asyncio


class CommandLoader:

    def __init__(self, client):
        # Public
        self.client = client

        # Private
        # List of commands to load
        self.__command = [
            # Command
            "command.mod", "command.start", "command.summon",
            "command.profile", "command.inventory",

            # Event
            "utility.event.on_ready", "utility.event.on_error"
        ]

    async def load_commands(self):
        """
        Load all the commands stored in the command attribute

        --

        :return: `None`
        """

        for command in self.__command:
            await asyncio.sleep(0)

            self.client.load_extension(command)

        return
