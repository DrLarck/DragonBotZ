"""
Summon command

--

Author : DrLarck

Last update : 20/03/20 by DrLarck
"""

from discord.ext import commands

# util
from utility.command.checker import CommandChecker
from utility.entity.banner import BannerGetter


class CommandSummon(commands.Cog):

    def __init__(self, client):
        self.client = client

        # Private
        self.__cost = 5
        self.__getter = BannerGetter()

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.command()
    async def summon(self, context, banner_reference: int = 1):

        # Init
        banner = await self.__getter.get_banner(banner_reference)

        if banner is not None:
            summoned = await banner.summon()

            character_display = await summoned.get_display_card(self.client)

            await context.send(embed=character_display)

        else:
            await context.send(f"Banner **{banner_reference:,}** not found")


def setup(client):
    client.add_cog(CommandSummon(client))