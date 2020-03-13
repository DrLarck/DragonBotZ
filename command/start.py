"""
Start command

--

Author : DrLarck

Last update : 13/03/20 by DrLarck
"""

import time

from discord.ext import commands

# util
from utility.player import Player
from utility.database import Database
from utility.command.checker import CommandChecker


class CommandStart(commands.Cog):

    def __init__(self, client):
        # Public
        self.client = client

        # Private
        self.__start_dragonstone = 50
        self.__start_zenis = 100000

    @commands.check(CommandChecker.can_register)
    @commands.command()
    async def start(self, context):
        """
        Register the player into the database

        :param context: (`discord.ext.commands.Context`)

        --

        :return: `None`
        """

        # Init
        player = Player(context.message.author)
        date = time.strftime("%d/%m/%y - %H:%M", time.gmtime())
        database = Database()

        # Register the player into the database
        await database.execute("""
                               INSERT INTO player_info(
                               player_id, player_name,
                               player_register_date, player_language)
                               VALUES($1, $2, $3, $4);
                               """, [player.id, player.name, date, 'EN'])

        return


def setup(client):
    client.add_cog(CommandStart(client))

