"""
Command logger

--

Author : DrLarck

Last update : 21/03/20 by DrLarck
"""

import asyncio
import time


class CommandLogger:

    def __init__(self, client):
        # Private
        self.__database = client.database

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

            # Get the parameter
            current_param = command_param[i]

            # Ignore the parameter if it's NoneType
            if current_param is not None:
                # Convert the param to str
                current_param = str(current_param)

                # Check if we need to add a comma or not
                if i == len(command_param) - 1:  # If we reach the end of the list
                    # Do not add the final comma
                    parameter += current_param

                else:  # Add a comma
                    parameter += current_param + ', '  # Add a comma between each parameter

        # Writing log
        await self.__database.execute("""INSERT INTO command_log(
                                      command, parameter, date, 
                                      time, caller_id, caller_name, message)
                                      VALUES($1, $2, $3, $4, $5, $6, $7);""",
                                      [command_name, parameter, command_date,
                                       command_time, command_author.id, command_author.name,
                                       command_message.content])

        return 
