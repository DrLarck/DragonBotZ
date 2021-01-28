"""Mod commands

@author : DrLarck

@update : 28/01/21 by DrLarck"""

import discord

from discord.ext import commands

from utility.command.checker import CommandChecker

from utility.entity.player import Player
from utility.graphic.icon import GameIcon


class CommandMod(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.i = GameIcon()

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.is_mod)
    @commands.group(invoke_without_command=True)
    async def mod(self, context):
        """Displays the mod help"""

        return
    
    @mod.group()
    async def give(self, context):
        """Display the mod give help"""
        
        return
    
    @give.command(aliases=["ds"])
    async def dragonstone(self, context, amount: int, target: discord.Member):
        """Give the amount of ds to the target"""

        player = Player(context, self.client, target)

        await player.resource.add_dragonstone(amount)

        await context.send(f"You've successfully sent {amount:,} {self.i.dragonstone} to {player.name}")
    
    @give.command(aliases=["z"])
    async def zenis(self, context, amount: int, target: discord.Member):
        """Give the amount of zenis to the target"""

        player = Player(context, self.client, target)

        await player.resource.add_zeni(amount)

        await context.send(f"You've successfully sent {amount:,} {self.i.zeni} to {player.name}")
        

def setup(client):
    client.add_cog(CommandMod(client))
