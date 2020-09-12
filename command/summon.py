"""
Summon command

--

Author : DrLarck

Last update : 12/09/20 by DrLarck
"""
import asyncio

from discord.ext import commands

# util
from utility.command.checker import CommandChecker
from utility.entity.banner import BannerGetter
from utility.entity.player import Player
from utility.graphic.icon import GameIcon
from utility.graphic.color import GameColor
from utility.graphic.embed import CustomEmbed


class CommandSummon(commands.Cog):

    def __init__(self, client):
        self.client = client

        # Private
        self.__cost = 5
        self.__getter = BannerGetter()

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.command(aliases=["sum"])
    async def summon(self, context, banner_reference: int = None):

        # Log
        await self.client.logger.log(context)

        # Init
        player = Player(context, self.client, context.message.author)
        icon = GameIcon()

        # Get the banner
        if banner_reference is None:  # If the banner reference is not specified
            banner = await self.__getter.get_current_banner()

        # If the banner reference is specified
        else:
            banner = await self.__getter.get_banner(banner_reference)

        # Check if the player has enough resource to summon
        player_dargonstone = await player.resource.get_dragonstone()

        # If the player has enough to summon
        if player_dargonstone >= self.__cost and banner is not None:
            # Get the summoned character
            summoned = await banner.summon()

            # Setup the embed
            character_display = await summoned.get_display_card(self.client)
            character_display.set_thumbnail(url=player.avatar)
            character_display.description = f"Summoned from **{banner.name}** banner"

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

            await player.experience.add_power(2)

        # If the banner has not been found
        elif banner is None:
            await context.send(f"Banner **{banner_reference:,}** not found")

        # If the player doesn't have enough resources
        else:
            await context.send(f"You do not have enough **Dragon stones**{icon.dragonstone} to summon")

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=["ms"])
    async def multisummon(self, context):
        """Allows the player to do a multisummon"""

        # Log
        await self.client.logger.log(context)

        # Init
        player = Player(context, self.client, context.message.author)
        icon = GameIcon()
        color = GameColor()

        # Check if the player has enough resource to proceed
        # a multisummon
        player_ds = await player.resource.get_dragonstone()
        banner = await self.__getter.get_current_banner()

        if player_ds >= self.__cost * 10:
            summoned = await banner.multi_summon()
            summon_content = ""

            high_rarity = summoned[0].rarity.value
            for character in summoned:
                await asyncio.sleep(0)

                if character.rarity.value > high_rarity:
                    high_rarity = character.rarity.value

                summon_content += f"`#{character.id}`- {character.rarity.icon} **{character.name}**\n"

                await self.client.database.execute("""
                                                   INSERT INTO character_unique(
                                                   character_reference, character_owner_id, character_owner_name,
                                                   character_rarity)
                                                   VALUES($1, $2, $3, $4);
                                                   """, [character.id, player.id, player.name, character.rarity.value])

            summon_color = await color.get_rarity_color(high_rarity)

            embed = await CustomEmbed().setup(
                self.client, title=f"{player.name}'s multi summon",
                color=summon_color, thumbnail_url=player.avatar
            )

            embed.add_field(
                name="Content :",
                value=summon_content,
                inline=False
            )

            await context.send(embed=embed)

            # Remove resource
            await player.resource.remove_dragonstone(self.__cost * 10)

            # Generate an unique id
            await banner.set_unique_id(self.client)

            await player.experience.add_power(20)

        else:
            await context.send(f"You do not have enough **Dragon stones**{icon.dragonstone} to summon")


def setup(client):
    client.add_cog(CommandSummon(client))
