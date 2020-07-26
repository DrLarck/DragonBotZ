"""
On client ready event handler

--

Author : DrLarck

Last update : 26/07/20 by DrLarck
"""

from discord.ext import commands


class EventOnReady(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Prints a message when the client is ready

        --

        :return: `None`
        """

        # Init
        guilds = len(self.client.guilds)

        print(f"""
########################################
########################################
###                                  ###        
##    - DISCORD BALL Z : ORIGINS -    ##
##            - READY -               ##
###                                  ###  
########################################
########################################
########################################
########################################
###                                  ###
##                                    ##
              • Guilds : {guilds:,}
##                                    ##
###                                  ###
########################################
########################################""")

        return


def setup(client):
    client.add_cog(EventOnReady(client))
