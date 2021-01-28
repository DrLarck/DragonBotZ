"""Premium command

@author : DrLarck

@update : 28/01/21 by DrLarck"""

from discord.ext import commands

from utility.command.checker import CommandChecker
from utility.graphic.embed import CustomEmbed


class CommandPremium(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.check(CommandChecker.game_ready)
    @commands.command(aliases=["donate"])
    async def premium(self, context):
        embed = await CustomEmbed().setup(
            self.client, title="Premium"
        )

        text = "Become a **Patron**, claim the **LR** card of your choice and get really interesting boosts !\n\n[Click here to support the project !](https://www.patreon.com/discordballz)"

        embed.add_field(
            name="Become a Patron",
            value=text
        )

        await context.send(embed=embed)


def setup(client):
    client.add_cog(CommandPremium(client))
