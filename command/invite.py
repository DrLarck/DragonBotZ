"""Invite command

@author : DrLarck

@update : 28/01/21 by DrLarck"""

from discord.ext import commands

from utility.command.checker import CommandChecker
from utility.graphic.embed import CustomEmbed


class CommandInvite(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.check(CommandChecker.game_ready)
    @commands.command(aliases=["add"])
    async def invite(self, context):
        embed = await CustomEmbed.setup(
            self.client, title="Invite Dragon Bot Z"
        )

        invite = "[Click here to invite Dragon Bot Z to your server !](https://discord.com/oauth2/authorize?=&client_id=529730466442510346&scope=bot&permissions=1141238977)"

        embed.add_field(
            name="Invite Dragon Bot Z to your server !",
            value=invite
        )

        await context.send(embed=embed)


def setup(client):
    client.add_cog(CommandInvite(client))
