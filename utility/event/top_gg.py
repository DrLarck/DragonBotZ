"""Top.gg integration https://github.com/top-gg/python-sdk

- Contains integrated webhook

- Auto server count post

@author DrLarck

@update 19/01/20 by DrLarck"""

import os
import dbl
import discord

from discord.ext import commands
from utility.entity.player import Player
from utility.graphic.icon import GameIcon


class TopGgWebhook(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.token = os.environ["dev_dbz_dbl_token"]
        self.dbl = dbl.DBLClient(
            self.client, self.token, 
            webhook_path="/dblwebhook", 
            webhook_port=8152,
            webhook_auth=self.token
        )
    
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        """Triggered when a vote is cast on top.gg

        @param data - `dict`

        @return - `None`"""

        weekend = data["isWeekend"]
        icon = GameIcon()
        user_id = int(data["user"])

        # Rewards
        reward_ds = 25
        reward_zenis = 1000
        reward_power = 100

        # If it's weekend, rewards are doubled
        if weekend:
            reward_ds *= 2
            reward_zenis *= 2
            reward_power *= 2

        player = await Player(None, self.client, None).get_player_from_id(
            user_id
        )

        if player is not None:
            # Sends rewards to the player
            await player.resource.add_dragonstone(reward_ds)
            await player.resource.add_zeni(reward_zenis)
            await player.experience.add_power(reward_power)

            # Send dm
            user = await self.client.get_user(user_id)

            try:
                await user.send(f"Thanks for voting ! Here are **{reward_ds}**{icon.dragonstone}, as well as **{reward_zenis}**{icon.zenis} and **{reward_power}**:star:")
            
            except discord.Forbidden:
                print(f"Failed to send reward message to {user_id} : Permission denied")
                pass

            except discord.HTTPException:
                print(f"Failed to send reward message to {user_id}")
                pass
                
            else:
                pass
        
        return

def setup(client):
    client.add_cog(TopGgWebhook(client))
