"""Allow the player to manage his team

--

@author DrLarck

@update 29/07/20 by DrLarck"""

import asyncio

from discord.ext import commands
from utility.command.checker import CommandChecker
from utility.entity.player import Player
from utility.graphic.embed import CustomEmbed


class CommandTeam(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.group(invoke_without_command=True)
    async def team(self, context):
        """Allow the player to display his team"""
        
        player = Player(context, self.client, context.message.author)
        team_ = await player.combat.get_team()

        embed = await CustomEmbed().setup(
            self.client, title=f"{player.name}'s team",
            thumbnail_url=player.avatar
            )
        
        # Display the player's team
        team_display = ""
        letters = ['A', 'B', 'C']
        
        if len(team_) > 0:
            for i in range(len(letters)):
                await asyncio.sleep(0)

                # If the player has no more fighters
                if i > len(team_):
                    team_display += f"{letters[i]} : **--**\n"
                
                else:
                    character = team_[i]
                    lvl = character.level
                    team_display += f"{letters[i]} : **{character.name}**{character.type.icon} - lv.**{lvl:,}**\n"
        
        # Team empty
        else:
            team_display = f"A : **--**\nB : **--**\nC : **--**"

        embed.add_field(name="Fighters", value=team_display, inline=False)

        await context.send(embed=embed)
        

def setup(client):
    client.add_cog(CommandTeam(client))
