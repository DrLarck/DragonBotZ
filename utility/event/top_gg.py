"""Top.gg integration https://github.com/top-gg/python-sdk

- Contains integrated webhook

- Auto server count post

@author DrLarck

@update 18/01/20 by DrLarck"""

import os

from discord.ext import commands
import dbl


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

        print(data)

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        """Triggered when a test is cast

        @param data - `dict` 

        @return - `None`"""

        print("test", data)


def setup(client):
    client.add_cog(TopGgWebhook(client))
