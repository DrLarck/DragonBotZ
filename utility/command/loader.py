"""
Command loader

--

Author : DrLarck

Last update : 28/01/21 by DrLarck
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
            "command.help", "command.start", "command.summon",
            "command.profile", "command.inventory", "command.box",
            "command.character",
            "command.hourly", "command.daily", "command.status",
            "command.team", "command.train", "command.mission",
            "command.recycle", "command.shop", "command.trade",
            "command.vote", "command.invite", "command.mod",
            "command.premium",

            # Event
            "utility.event.on_ready", "utility.event.on_error", 
            "utility.event.top_gg"
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
