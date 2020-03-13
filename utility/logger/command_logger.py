"""
Command logger

--

Author : DrLarck

Last update : 13/03/20 by DrLarck
"""

import asyncio
import time

from utility.database import Database


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
        command_param = context.args
        command_date = time.strftime("%d/%m/%y - %H:%M", time.gmtime())  # Get the date and the hour
        command_time = time.time()  # Get the full time as second since epoch
        command_message = context.message
        command_author = command_message.author

        # Set the param as str
        parameter = ""

        # The first two parameters are :
        # - The command Object
        # - The Context
        # The 'real' parameters are stored
        # At the index >= 2
        for i in range(2, len(command_param)):
            await asyncio.sleep(0)

            parameter += command_param[i] + ', '  # Add a comma between each parameter

        # Writing log
        await self.__database.execute("""INSERT INTO command_log(
                                      command, parameter, date, 
                                      time, caller_id, caller_name, message)
                                      VALUES($1, $2, $3, $4, $5, $6, $7);""",
                                      [command_name, parameter, command_date,
                                       command_time, command_author.id, command_author.name,
                                       command_message.content])

        return 
