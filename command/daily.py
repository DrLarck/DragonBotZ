"""
Daily command

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
from utility.command.tool.tool_time import ToolTime


class CommandDaily(commands.Cog):

    def __init__(self, client):
        self.client = client

        # Private
        self.__dragonstone = 25
        self.__zeni = 50000
        self.__experience = 0
        self.__combo_rate = 1.05
        self.__toll_time = ToolTime()

        self.__time_daily = 86400
        self.__time_combo = 172800

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.command()
    async def daily(self, context):
        # Log
        await self.client.logger.log(context)

        # Init
        player = Player(context, self.client, context.message.author)
        current_time = time.time()
        icon = GameIcon()

        # Get the player's last daily
        player_daily = await player.time.get_daily()

        # The player has 47h59 to do his combo
        elapsed = current_time - player_daily

        # A day has passed
        # Time in seconds
        if elapsed >= self.__time_daily:
            # Init
            combo = 0

            # The player is on a combo streak
            if elapsed < self.__time_combo:
                # Get the combo value
                combo = await player.time.get_daily_combo()

                # Increase the combo
                combo += 1

            # Get the rewards value
            reward_ds = int(self.__dragonstone * pow(self.__combo_rate, combo))
            reward_zeni = int(self.__zeni * pow(self.__combo_rate, combo))
            reward_xp = int(self.__experience * pow(self.__combo_rate, combo))

            # Update the player_time table
            await player.time.update_daily_time(current_time)
            await player.time.update_daily_combo(combo)

            # Update the player resources
            await player.resource.add_dragonstone(reward_ds)
            await player.resource.add_zeni(reward_zeni)

            # Rewarding message
            message = f"""
Daily : **+{reward_ds:,}**{icon.dragonstone}, **+{reward_zeni:,}**{icon.zeni}, **+{reward_xp:,}**:star: 
*(Combo **x{combo}**)*"""

            await context.send(message)

        # No the time yet
        else:
            time_remaining = self.__time_daily - elapsed

            # Get the string that tells when the player has to come back
            come_back = await self.__toll_time.convert_time(time_remaining)

            await context.send(f"It's to early for this, come back in **{come_back}**")


def setup(client):
    client.add_cog(CommandDaily(client))
