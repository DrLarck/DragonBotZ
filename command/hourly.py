"""
Hourly command

--

Author : DrLarck

Last update : 08/04/20 by DrLarck
"""

import time

from discord.ext import commands

# util
from utility.command.checker import CommandChecker
from utility.entity.player import Player
from utility.graphic.icon import GameIcon

# tool
from utility.command.tool.tool_time import ToolTime


class CommandHourly(commands.Cog):

    def __init__(self, client):
        self.client = client

        # Private
        self.__dragonstone = 5
        self.__zeni = 10000
        self.__experience = 0
        self.__combo_rate = 1.2  # +20 %
        self.__tool_time = ToolTime()

        self.__time_hourly = 3600
        self.__time_combo = 7200

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.command()
    async def hourly(self, context):
        # Log
        await self.client.logger.log(context)

        # Init
        player = Player(self.client, context.message.author)
        current_time = time.time()
        icon = GameIcon()

        # Get the player's last hourly
        player_hourly = await player.time.get_hourly()

        # If there is more than 1 hour between the current time and the player's
        # last hourly : do the hourly
        # The player has 1h59 to do his hourly to gain a combo point
        elapsed = current_time - player_hourly

        # If an hour has passed
        # Time is in seconds
        if elapsed >= self.__time_hourly:
            # Init
            combo = 0

            # The player is on a combo streak
            if elapsed < self.__time_combo:
                # Get the combo value
                combo = await player.time.get_hourly_combo()

                # Increase the combo
                combo += 1

            # Get the rewards value
            reward_ds = int(self.__dragonstone * pow(self.__combo_rate, combo))
            reward_zeni = int(self.__zeni * pow(self.__combo_rate, combo))
            reward_xp = int(self.__experience * pow(self.__combo_rate, combo))

            # Update the player_time table
            # Time
            await player.time.update_hourly_time(current_time)

            # Combo
            await player.time.update_hourly_combo(combo)

            # Update the player resources
            await player.resource.add_dragonstone(reward_ds)
            await player.resource.add_zeni(reward_zeni)

            # Rewarding message
            message = f"""
Hourly : **+{reward_ds:,}**{icon.dragonstone}, **+{reward_zeni:,}**{icon.zeni}, **+{reward_xp:,}**:star: 
*(Combo **x{combo}**)*"""

            await context.send(message)

        # Not the time yet
        else:
            time_remaining = self.__time_hourly - elapsed

            # Get the string that tells when the player has to come back
            come_back = await self.__tool_time.convert_time(time_remaining)

            await context.send(f"It's to early for this, come back in **{come_back}**")


def setup(client):
    client.add_cog(CommandHourly(client))
