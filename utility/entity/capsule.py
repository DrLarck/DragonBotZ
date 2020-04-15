"""Represent a capsule

--

Author : DrLarck

Last update : 15/04/20 by DrLarck"""

import random
import asyncio

# util
from utility.graphic.icon import GameIcon

# tool
from utility.global_tool import GlobalTool


class Capsule:

    def __init__(self, context, client, player):
        """:param context: (`discord.ext.commands.Context`)
           
           :param client: (`discord.ext.commands.Bot`)

           :param player: (`Player`)"""

        # Public
        self.client = client
        self.context = context
        self.player = player
        self.game_icon = GameIcon()

        # Info
        self.name = ""
        self.icon = ""
        self.reference = 0
        self.unique_id = ""

        # Rewards
        self.dragonstone = 0
        self.zeni = 0
        self.experience = 0
        self.item = []

        # Rate
        # As %
        # One of the rates must be 100 as we eliminate
        self.rate_dragonstone = 0
        self.rate_zeni = 0
        self.rate_experience = 0
        self.rate_item = 0

        # Reward gap
        self.reward_gap = 0.9  # 10 %

        # Private
        self.__database = self.client.database
        self.__global_tool = GlobalTool()

        # Generation %
        self.__gen_n = 100
        self.__gen_r = 66
        self.__gen_sr = 33
        self.__gen_ssr = 16.5
        self.__gen_ur = 8.25
        self.__gen_lr = 3

    # Public method
    async def open(self):
        """Open the capsule and send the reward to the player

        --

        :return: `None`"""

        # Init
        icon, name, qt = "", "", 0
        rewarded = False

        # Get the player's roll
        roll = random.uniform(0, 100)

        # Check if the item list is not empty
        if len(self.item) > 0:
            # Check if the player has loot a training item
            if roll <= self.rate_item and rewarded is False:
                item = random.choice(self.item)

                # Set the item
                item = item(self.client)

                # Setup the reward info
                name = item.name
                icon = item.icon

                # Add the item into the database
                await self.player.item.add_training_item(item.reference)

                rewarded = True

        # Check the ds loot
        if roll <= self.rate_dragonstone and rewarded is False:
            # Generate a ds reward
            qt = random.randint(self.dragonstone * self.reward_gap, self.dragonstone)

            # Setup the reward info
            name = "Dragon Stones"
            icon = self.game_icon.dragonstone

            # Add the reward into the player's inventory
            await self.player.resource.add_dragonstone(qt)

            rewarded = True

        # Check the zenis loot
        if roll <= self.rate_zeni and rewarded is False:
            # Generate the zeni reward
            qt = random.randint(self.zeni * self.reward_gap, self.zeni)

            # Setup the reward info
            name = "Zenis"
            icon = self.game_icon.zeni

            # Add the reward into the player's inventory
            await self.player.resource.add_zeni(qt)

            rewarded = True

        # Delete the capsule
        await self.delete()

        # Display the message
        if qt > 0:
            msg = f"You've opened a {self.icon}**{self.name}** capsule and found **{qt:,}**{icon}"

        else:
            msg = f"You've opened a {self.icon}**{self.name}** capsule and found {icon}**{name}**"

        await self.context.send(msg)

        return

    async def set_unique_id(self):
        """
        Generate an unique id for the capsule that have 'NONE' as unique id

        --

        :return: `None`
        """

        # Get the capsule that have 'NONE' as unique id
        capsules = await self.__database.fetch_row("""
                                                   SELECT reference
                                                   FROM capsule
                                                   WHERE unique_id = 'NONE';
                                                   """)

        # Generate an unique id for each of those capsules
        for capsule in capsules:
            await asyncio.sleep(0)

            # Get the capsule reference
            reference = capsule[0]
            unique_id = await self.__global_tool.generate_unique_id(reference)

            # Update the id
            await self.__database.execute("""
                                          UPDATE capsule
                                          SET unique_id = $1
                                          WHERE reference = $2;
                                          """, [unique_id, reference])

        return

    async def get_capsule_by_reference(self, reference):
        """
        Return a capsule object according to the passed reference

        :param reference: (`int`)

        --

        :return: `Capsule` or `None` if not found
        """

        # Init
        capsule = None

        if reference is 0:
            from utility.entity.item.capsule.capsule_0 import CapsuleN

            capsule = CapsuleN(self.context, self.client, self.player)

        return capsule

    async def delete(self):
        """
        Delete the capsule from the database

        --

        :return: `None`
        """

        await self.__database.execute("""
                                      DELETE FROM capsule
                                      WHERE unique_id = $1;
                                      """, [self.unique_id])

        return
