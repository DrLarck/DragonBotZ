"""Vote command

@author : DrLarck

@update : 27/01/21 by DrLarck"""

from discord.ext import commands

from utility.graphic.embed import CustomEmbed
from utility.command.checker import CommandChecker
from utility.graphic.icon import GameIcon


class CommandVote(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.check(CommandChecker.game_ready)
    @commands.command()
    async def vote(self, context):
        
        embed = await CustomEmbed().setup(
            self.client, title="Vote for Dragon Bot Z"
        )

        i_d = GameIcon().dragonstone
        i_z = GameIcon().zeni

        vote_message = f"Vote for Dragon Bot Z to get rewards ! Double rewards on weekend !\n**25** {i_d}, **1,000** {i_z}, **100** :star:\n\n[Click here to vote !](https://top.gg/bot/529730466442510346/vote)"

        embed.add_field(name="Vote", value=vote_message)

        await context.send(embed=embed)


def setup(client):
    client.add_cog(CommandVote(client))
