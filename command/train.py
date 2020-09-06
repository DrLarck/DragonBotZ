"""Allow the player to train his characters

--

@author DrLarck

@update 06/09/20 by DrLarck"""

import asyncio
import random

from discord.ext import commands

# util
from utility.command.checker import CommandChecker
from utility.command.tool.tool_train import ToolTrain

from utility.entity.player import Player
from utility.entity.CPU import CPU
from utility.entity.combat import Combat
from utility.entity.character import CharacterGetter, CharacterExperience
from utility.global_tool import GlobalTool


class CommandTrain(commands.Cog):

    def __init__(self, client):
        self.client      = client
        self.tool        = ToolTrain(self.client)
        self.global_tool = GlobalTool()

        # Rewards
        self.reward_experience = 45

    @commands.check(CommandChecker.game_ready)
    @commands.check(CommandChecker.register)
    @commands.check(CommandChecker.not_fighting)
    @commands.check(CommandChecker.has_team)
    @commands.command()
    async def train(self, context):
        """Allow the player to train his characters"""

        # Log
        await self.client.logger.log(context)

        player   = Player(context, self.client, context.message.author)
        premium_bonus = await self.global_tool.get_player_premium_resource_bonus(player)
        cpu      = CPU(context, self.client, context.message.author)
        cpu.name = "Trainer"

        # Set the CPU's team
        opponent_team, level_range = await self.tool.generate_opponent_team(player)
        
        await cpu.set_team(opponent_team, level_range)

        combat = Combat(self.client, context, player, cpu)

        # Run the combat
        winner = await combat.run()
        
        # Display the winner name
        message = f"🏆 **{winner.name}** has won the fight ! "

        await context.send(message)

        # If the winner is a player, grant xp to his team
        if winner is player:
            exp_message   = ""
            unique_ids    = player.combat.unique_id_team
            exp_manager   = CharacterExperience(self.client)
            charar_getter = CharacterGetter()
            await player.experience.add_power(5)

            for character in unique_ids:
                await asyncio.sleep(0)

                # Get the character's data
                character_data = await charar_getter.get_from_unique(self.client, self.client.database, character)

                # Generate an exp amount
                exp_amount = random.randint(int(self.reward_experience * 0.75), self.reward_experience)
                exp_amount = int(await self.tool.generate_exp_reward(exp_amount, character_data.level) * premium_bonus)
                
                # Add exp to the character and check if it leveled up
                new_level = await exp_manager.add_experience(character, exp_amount)
                                        
                # If the character had leveled up
                if new_level is not None:
                    exp_message += f":star: **{character_data.name}**{character_data.type.icon} has won **{exp_amount:,}**xp and reached the level **{new_level:,}**\n"
                
                else:
                    exp_message += f":star: **{character_data.name}**{character_data.type.icon} has won **{exp_amount:,}**xp\n"
        
            await context.send(exp_message)


def setup(client):
    client.add_cog(CommandTrain(client))
