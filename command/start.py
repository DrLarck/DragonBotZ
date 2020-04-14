"""
Start command

--

Author : DrLarck

Last update : 08/04/20 by DrLarck
"""

import time

from discord.ext import commands

# util
from utility.entity.player import Player
from utility.command.checker import CommandChecker
from utility.logger.command_logger import CommandLogger
from utility.graphic.icon import GameIcon


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
        player = Player(context, self.client, context.message.author)
        date = time.strftime("%d/%m/%y - %H:%M", time.gmtime())
        database = self.client.database
        await CommandLogger(self.client).log(context)

        # Register the player into the database
        await database.execute("""
                               INSERT INTO player_info(
                               player_id, player_name,
                               player_register_date, player_language)
                               VALUES($1, $2, $3, $4);
                               """,
                               [player.id, player.name, date, 'EN'])

        await database.execute("""
                                INSERT INTO player_resource(
                                player_id, player_name,
                                player_dragonstone, player_zeni)
                                VALUES($1, $2, $3, $4);
                                """,
                               [player.id, player.name, self.__start_dragonstone, self.__start_zenis])

        await database.execute("""
                               INSERT INTO player_experience(
                               player_id, player_name)
                               VALUES($1, $2);
                               """, [player.id, player.name])

        await database.execute("""
                               INSERT INTO player_time(
                               player_id, player_name)
                               VALUES($1, $2);
                               """, [player.id, player.name])

        # Display a welcome message
        await context.send(f"""
Welcome to **Discord Ball Z : Origins** ! We're hoping you to enjoy your adventure !

You receive **{self.__start_dragonstone:,}**{GameIcon().dragonstone} and **{self.__start_zenis:,}**{GameIcon().zeni}.
Those will allow you to **summon** or **buy** powerful heroes who will fight for you !

Do not hesitate to use the `d!help` command or join the **Official Support server** : https://discord.gg/eZf2p7h""")

        return


def setup(client):
    client.add_cog(CommandStart(client))

