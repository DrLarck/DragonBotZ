"""Patreon support

--

@author DrLarck

@update 04/09/20 by DrLarck"""

import patreon
import os
import asyncio


class Patreon:

    def __init__(self):
        self.client = None
    
    async def init(self, access_token):
        """Init the Patreon api

        @param str access_token

        --

        @return None"""

        # Init the patreon api client
        if self.client is None:
            self.client = patreon.API(access_token)

        return
    
    async def get_all_patrons(self):
        """Get the list of all patrons

        --

        @return list"""

        # If the client doesn't exist
        if self.client is None:
            print("Error : Patron API client not defined")
            return

        patrons = []

        # Get the campaign id
        campaign_resource = self.client.fetch_campaign()
        campaign_id       = campaign_resource.data()[0].id()

        # Get all the pledgers
        all_pledgers = []    # Contains the list of all pledgers
        cursor       = None  # Allows us to walk through pledge pages
        stop         = False

        while not stop:
            # Get the resources of the current pledge page
            # Each page contains 25 pledgers, also
            # fetches the pledge info such as the total
            # $ sent and the date of pledge end
            pledge_resource = self.client.fetch_page_of_pledges(
                campaign_id, 25,
                cursor=cursor, 
                fields={
                    "pledge": ["total_historical_amount_cents", "declined_since"]
                }
            )

            # Update cursor
            cursor = self.client.extract_cursor(pledge_resource)

            # Add data to the list of pledgers
            all_pledgers += pledge_resource.data()

            # If there is no more page, stop the loop
            if not cursor:
                stop = True
                break

        # Get the pledgers info and add the premium status
        for pledger in all_pledgers:
            await asyncio.sleep(0)

            reward_tier = 0
            total_paid  = 0

            # Get the date of declined pledge
            # False if the pledge has not been declined
            declined_since = pledger.attribute("declined_since")
            total_paid     = pledger.attribute("total_historical_amount_cents") / 100

            # Get the pledger's discord ID
            pledger_id = pledger.relationship("patron").attribute("social_connections")["discord"]["user_id"]

            # Get the reward tier of the player
            if pledger.relationships()["reward"]["data"]:
                reward_tier = int(pledger.relationship("reward").attribute("amount_cents") / 100)

            print(pledger.relationship("patron").attribute("first_name"), reward_tier, declined_since, total_paid)

        return patrons
