"""
Moderation commands

--

Author : DrLarck

Last update : 14/04/20 by DrLarck
"""

import asyncio

from discord.ext import commands

# util
from utility.logger.command_logger import CommandLogger
from utility.command.checker import CommandChecker
from utility.entity.player import Player


class CommandModeration(commands.Cog):

    def __init__(self, client):
        # Public
        self.client = client

    # Command
    @commands.check(CommandChecker.register)
    @commands.check(CommandChecker.no_dm)
    @commands.command()
    async def test(self, context):

        # Init
        await CommandLogger(self.client).log(context)

        player = Player(context, self.client, context.message.author)

        dragonstone = await player.resource.get_dragonstone()

        print(dragonstone)

        await player.resource.add_dragonstone(500)

        dragonstone = await player.resource.get_dragonstone()

        print(dragonstone)

    @commands.command()
    async def get_capsule(self, context):
        # log
        await self.client.logger.log(context)

        player = Player(context, self.client, context.message.author)

        await player.item.add_capsule(0)

    @commands.command()
    async def display_capsule(self, context):
        player = Player(context, self.client, context.message.author)
        capsules = await player.item.get_capsule()

        display = ""

        for capsule in capsules:
            await asyncio.sleep(0)

            display += f"{capsule.icon}{capsule.name}\n"

        await context.send(display)

    @commands.command()
    async def open(self, context, rarity: int):
        player = Player(context, self.client, context.message.author)

        await player.item.open_capsule(rarity)

    @commands.command()
    async def team(self, context):
        player = Player(context, self.client, context.message.author)

        player_team = await player.combat.get_team()

        for character in player_team:
            await asyncio.sleep(0)

            await context.send(character.name)


def setup(client):
    client.add_cog(CommandModeration(client))
