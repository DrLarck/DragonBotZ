"""
Represents the main class of the program.

--

Project start : 09/03/20

Author : DrLarck

Last update : 14/03/20 by DrLarck
"""

import discord
import os

from discord.ext import commands
from utility.command.loader import CommandLoader

# util
from utility.database import Database


class Main:

    def __init__(self):
        self.__TOKEN = os.environ["dev-dbz-token"]
        self.__version = "1.0.0.35"
        self.__phase = ["ALPHA", "BETA", "RELEASE", "STABLE"]

        self.__prefix = ["d!", "D!", "db", "Db"]

    def run(self):
        """
        Run the bot

        --

        :return: `None`
        """

        # Init
        activity = discord.Game(name=f"d!help | v{self.__version} - {self.__phase[0]}")
        
        client = commands.Bot(command_prefix=self.__prefix, help_command=None,
                              activity=activity)

        # Create the needed tables
        client.loop.run_until_complete(Database().create_game_tables())

        # Loading the commands
        client.loop.run_until_complete(CommandLoader(client).load_commands())

        # Run the bot
        client.run(self.__TOKEN)

        return


if __name__ == "__main__":  # If this file is the main file
    Main().run()
