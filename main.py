"""
Represents the main class of the program.

--

Project start : 09/03/20

Author : DrLarck

Last update : 09/03/20 by DrLarck
"""

import discord
import os

from discord.ext import commands


class Main:

    def __init__(self):
        self.__token = os.environ["dev-dbz-token"]
        self.__version = "1.0"
        self.__phase = ["ALPHA", "BETA", "RELEASE", "STABLE"]

    def run(self):
        """
        Run the bot

        --

        :return: `None`
        """

        # Init
        activity = discord.Game(name=f"d!help | v{self.__version} - {self.__phase[0]}")
        client = commands.Bot(command_prefix="!", help_command=None,
                              activity=activity)

        # Run the bot
        client.run(self.__token)

        return


if __name__ == "__main__":  # If this file is the main file
    Main().run()
