"""
Command logger

--

Author : DrLarck

Last update : 13/03/20 by DrLarck
"""

import time

from utility.database.database import Database


class CommandLogger:

    def __init__(self):
        # Private
        self.__database = Database()

    # Public
    async def log(self, context):
        """
        Log the command

        :param context:

        --

        :return: `None`
        """

        # Init
        command_name = context.command.name
        command_author = context.message.author

        

