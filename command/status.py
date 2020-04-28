"""
Status command

--

Author : DrLarck

Last update : 28/04/20 by DrLarck
"""

import asyncio
from discord.ext import commands

# util
from utility.command.checker import CommandChecker
from utility.graphic.embed import CustomEmbed


class CommandStatus(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.check(CommandChecker.game_ready)
    @commands.command()
    async def status(self, context):
        # Init
        embed = await CustomEmbed().setup(self.client,
                                          title="Game status", description="Display the status of each shard")

        # Get the current shard id
        current_shard = self.client.shard_id

        # Get the list of shards latencies
        shards_info = self.client.latencies

        display = f"Server's shard : #{current_shard}\n\n__Shards status__ :\n"

        # Get the display
        for shard in shards_info:
            await asyncio.sleep(0)

            # Id 0 : Shard id | Id 1 : Latency in seconds
            display += f"**Shard #{shard[0]} : {int(shard[1])}ms\n"

        # Setup the embed
        embed.add_field(name="Shards status",
                        value=display,
                        inline=False)

        await context.send(embed=embed)


def setup(client):
    client.add_cog(CommandStatus(client))
