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
from utility.entity.player import Player
from utility.graphic.icon import GameIcon


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
        player = Player(self.client, context.message.author)
        icon = GameIcon()
        banner = await self.__getter.get_banner(banner_reference)

        # Check if the player has enough resource to summon
        player_dargonstone = await player.resource.get_dragonstone()

        # If the player has enough to summon
        if player_dargonstone >= self.__cost and banner is not None:
            summoned = await banner.summon()

            character_display = await summoned.get_display_card(self.client)

            # Remove the amount of stones used
            await player.resource.remove_dragonstone(self.__cost)

            # Add the character to the character_unique table
            await self.client.database.execute("""
                                               INSERT INTO character_unique(
                                               character_reference, character_owner_id, character_owner_name,
                                               character_rarity) 
                                               VALUES($1, $2, $3, $4);
                                               """, [summoned.id, player.id, player.name, summoned.rarity.value])

            # Generate an unique id
            await banner.set_unique_id(self.client)
            
            # Display the card
            await context.send(embed=character_display)

        # If the banner has not been found
        elif banner is None:
            await context.send(f"Banner **{banner_reference:,}** not found")

        # If the player doesn't have enough resources
        else:
            await context.send(f"You do not have enough **Dragon stones**{icon.dragonstone} to summon")


def setup(client):
    client.add_cog(CommandSummon(client))
