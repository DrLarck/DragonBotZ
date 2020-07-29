"""
Represents the main class of the program.

--

Project start : 09/03/20

Author : DrLarck

Last update : 29/07/20 by DrLarck
"""

import logging
import discord
import os

from discord.ext import commands

# util
from utility.entity.database import Database
from utility.logger.command_logger import CommandLogger
from utility.command.loader import CommandLoader
from utility.entity.character import CharacterGetter
from utility.entity.banner import BannerGetter


class Main:

    def __init__(self):
        self.__TOKEN = os.environ["dev_dbz_token"]
        self.__version = "2.1.0.159"
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
        
        client = commands.AutoShardedBot(command_prefix=self.__prefix, help_command=None,
                              activity=activity)

        logging.basicConfig(level=logging.INFO)

        # Create the database attribute for client
        client.database = Database()

        # Create the logger attribute for the client
        client.logger = CommandLogger(client)

        # Create the needed tables
        client.loop.run_until_complete(client.database.create_game_tables())

        # Filling up the cache
        client.loop.run_until_complete(CharacterGetter().set_cache(client))
        client.loop.run_until_complete(BannerGetter().set_cache(client))

        # Loading the commands
        client.loop.run_until_complete(CommandLoader(client).load_commands())

        # Run the bot
        client.run(self.__TOKEN)

        return


if __name__ == "__main__":  # If this file is the main file
    Main().run()
