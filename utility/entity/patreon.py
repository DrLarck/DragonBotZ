"""Patreon support

--

@author DrLarck

@update 24/01/21 by DrLarck"""

import patreon
import os
import asyncio
import time


class Patreon:

    def __init__(self, database):
        self.client = None
        self.database = database
    
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
            await asyncio.sleep(0)

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

            payment      = 0
            total_paid   = 0
            is_declined  = False
            pledger_tier = 0

            # Get the date of declined pledge
            # False if the pledge has not been declined
            declined_since = pledger.attribute("declined_since")
            total_paid     = pledger.attribute("total_historical_amount_cents") / 100

            # Get the pledger's discord ID
            discord_id = pledger.relationship("patron").attribute("social_connections")["discord"]["user_id"]

            # Get the reward tier of the player
            if pledger.relationships()["reward"]["data"]:
                payment = int(pledger.relationship("reward").attribute("amount_cents") / 100)
            
            # Find the tier index
            if payment <= 2.5:
                pledger_tier = 1
            
            elif payment > 2.5 and payment <= 4:
                pledger_tier = 2
            
            elif payment > 4 and payment <= 6:
                pledger_tier = 3
            
            elif payment > 6 and payment <= 10:
                pledger_tier = 4
            
            elif payment > 10 and payment <= 20:
                pledger_tier = 5
            
            elif payment > 20 and payment <= 50:
                pledger_tier = 6
            
            elif payment > 50:
                pledger_tier = 7

            # Check if the patron has declined his pledge
            if declined_since is not None:
                is_declined = True

            # Add patron data to the patrons list
            patrons.append(
                {
                    "name": pledger.relationship("patron").attribute("first_name"),
                    "tier": int(pledger_tier),
                    "payment": int(payment),
                    "declined": is_declined,
                    "total": int(total_paid),
                    "discord_id": int(discord_id)
                }
            )

        return patrons
    
    async def add_month(self, patron):
        """Add a premium month to a player

        @param dict patron

        --

        @returun None"""

        now = time.time()
        new = now + 2592000
        total_month = await self.database.fetch_value("""
                                                      SELECT player_premium_total_month
                                                      FROM player_info
                                                      WHERE player_id = $1;
                                                      """, [patron["discord_id"]]) 

        if total_month is not None:
            total_month += 1

        new_pledge_tier = patron["tier"]

        # Update player's premium data
        await self.database.execute("""
                                    UPDATE player_info
                                    SET player_premium_until = $1,
                                    player_premium_tier = $2,
                                    player_premium_total_month = $3
                                    WHERE player_id = $4;
                                    """, [new, new_pledge_tier, 
                                          total_month, patron["discord_id"]])
        
        # Check if the premium since is filled
        # if not, fill it with the current time
        premium_since = await self.database.fetch_value("""
                                                        SELECT player_premium_since
                                                        FROM player_info
                                                        WHERE player_id = $1;
                                                        """, [patron["discord_id"]])                                                   
        
        if premium_since is None or premium_since == 0:
            await self.database.execute("""
                                        UPDATE player_info
                                        SET player_premium_since = $1
                                        WHERE player_id = $2;                                                
                                        """, [now, patron["discord_id"]])

        return
    
    async def set_premium(self):
        """Set premium status for players

        --

        @return None"""

        # Retrieve all the patrons
        patrons  = await self.get_all_patrons()
        time_now = time.time()

        for patron in patrons:
            await asyncio.sleep(0)
            
            # Check if the player is premium
            is_premium = False
            premium_until = await self.database.fetch_value("""
                                                            SELECT player_premium_until
                                                            FROM player_info
                                                            WHERE player_id = $1;
                                                            """, [patron["discord_id"]])
            
            # If we have recorded data
            if premium_until is not None:
                if premium_until > time_now:
                    is_premium = True
            
            # If the player is already premium
            if is_premium:
                # Check if the pledge is not declined
                if not patron["declined"]:
                    # Check the date
                    limit_date = await self.database.fetch_value("""
                                                                 SELECT player_premium_until
                                                                 FROM player_info
                                                                 WHERE player_id = $1;
                                                                 """, [patron["discord_id"]])

                    # If the date is anterior, add a month
                    if limit_date < time_now:
                        await self.add_month(patron)

            # If the player is not premium
            else:
                # Check if declined
                if not patron["declined"]:
                    await self.add_month(patron)

        print("Premium : DONE")

        return
