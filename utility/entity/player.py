"""
Player object

--

Author : DrLarck

Last update : 14/04/20 by DrLarck
"""

import asyncio

# util
# items
from utility.entity.item.capsule.capsule_0 import CapsuleN


class Player:

    def __init__(self, client, user):
        # Public
        self.client = client
        self.name = user.name
        self.avatar = user.avatar_url
        self.id = user.id

        self.resource = PlayerResource(self)
        self.item = PlayerItem(self)
        self.experience = PlayerExperience(self)
        self.time = PlayerTime(self)


class PlayerResource:

    def __init__(self, player):
        # Private
        self.__database = player.client.database

        # Public
        self.player = player

    # Public Method
    async def get_resources(self):
        """
        Get the player's resources

        --

        :return: `list` | Index : 0 Dragon stones, 1 Zenis
        """

        resources = await self.__database.fetch_row("""
                                                    SELECT player_dragonstone, player_zeni 
                                                    FROM player_resource 
                                                    WHERE player_id = $1;
                                                    """, [self.player.id])

        return resources[0]

    async def get_dragonstone(self):
        """
        Get the player's dragon stone amount

        --

        :return: `int`
        """

        dragonstone = await self.__database.fetch_value("""
                                                        SELECT player_dragonstone 
                                                        FROM player_resource 
                                                        WHERE player_id = $1;
                                                        """, [self.player.id])

        return dragonstone

    async def get_zeni(self):
        """
        Get the player's zeni amount

        --

        :return: `int`
        """

        zeni = await self.__database.fetch_value("""
                                                SELECT player_zeni 
                                                FROM player_resource 
                                                WHERE player_id = $1;
                                                """, [self.player.id])

        return zeni

    async def add_dragonstone(self, amount):
        """
        Add the passed amount of dragonstone to the player resources

        :param amount: (`int`)

        --

        :return: `None`
        """

        # Init
        dragonstone = await self.get_dragonstone()

        # Add the amount of dragonstone
        dragonstone += amount

        # Update the inventory
        await self.__database.execute("""
                                      UPDATE player_resource 
                                      SET player_dragonstone = $1 
                                      WHERE player_id = $2;
                                      """, [dragonstone, self.player.id])

        return

    async def add_zeni(self, amount):
        """
        Add the passed amount of zeni to the player resources

        :param amount: (`int`)

        --

        :return: `None`
        """

        # Init
        zeni = await self.get_zeni()

        # Add the amount of zeni
        zeni += amount

        # Update the inventory
        await self.__database.execute("""
                                      UPDATE player_resource 
                                      SET player_zeni = $1 
                                      WHERE player_id = $2;
                                      """, [zeni, self.player.id])

        return

    async def remove_dragonstone(self, amount):
        """
        Remove a certain amount of dragon stones

        :param amount: (`int`)

        --

        :return: `None`
        """

        # Init
        dragonstone = await self.get_dragonstone()

        # Remove the amount
        dragonstone -= amount

        # Update the inventory
        await self.__database.execute("""
                                      UPDATE player_resource
                                      SET player_dragonstone = $1
                                      WHERE player_id = $2;
                                      """, [dragonstone, self.player.id])

        return

    async def remove_zeni(self, amount):
        """
        Remove a certain amount of zeni

        :param amount: (`int`)

        --

        :return:
        """

        # Init
        zeni = await self.get_zeni()

        # Remove the amount
        zeni -= amount

        # Update inventory
        await self.__database.execute("""
                                      UPDATE player_resource
                                      SET player_zeni = $1
                                      WHERE player_id = $2;
                                      """, [zeni, self.player.id])

        return


class PlayerExperience:

    def __init__(self, player):
        # Private
        self.__database = player.client.database

        # Public
        self.player = player

    # Public
    async def get_player_level(self):
        """
        Get the player level from the database

        --

        :return: `int`
        """

        player_level = await self.__database.fetch_value("""
                                                         SELECT player_level 
                                                         FROM player_experience
                                                         WHERE player_id = $1;   
                                                         """, [self.player.id])

        return player_level


class PlayerTime:

    def __init__(self, player):
        # Private
        self.__database = player.client.database

        # Public
        self.player = player

    # Public
    async def get_hourly(self):
        """
        Get the time when the player did his last hourly

        --

        :return: `int`
        """

        # Init
        last_hourly = await self.__database.fetch_value("""
                                                        SELECT player_hourly_time
                                                        FROM player_time
                                                        WHERE player_id = $1;
                                                        """, [self.player.id])

        return last_hourly

    async def get_daily(self):
        """
        Get the time when the player did his last daily

        --

        :return: `int`
        """

        # Init
        last_daily = await self.__database.fetch_value("""
                                                       SELECT player_daily_time
                                                       FROM player_time
                                                       WHERE player_id = $1;
                                                       """, [self.player.id])

        return last_daily

    async def get_hourly_combo(self):
        """
        Get the player's hourly combo

        --

        :return: `int`
        """

        # Init
        hourly_combo = await self.__database.fetch_value("""
                                                         SELECT player_hourly_combo
                                                         FROM player_time
                                                         WHERE player_id = $1;
                                                         """, [self.player.id])

        return hourly_combo

    async def get_daily_combo(self):
        """
        Get the player's daily combo

        --

        :return: `int`
        """

        # Init
        daily_combo = await self.__database.fetch_value("""
                                                        SELECT player_daily_combo
                                                        FROM player_time
                                                        WHERE player_id = $1;
                                                        """, [self.player.id])

        return daily_combo

    async def update_hourly_combo(self, value):
        """
        Update the player's hourly combo value

        :param value: (`int`)

        --

        :return: `None`
        """

        await self.__database.execute("""
                                      UPDATE player_time
                                      SET player_hourly_combo = $1
                                      WHERE player_id = $2;
                                      """, [value, self.player.id])

        return

    async def update_daily_combo(self, value):
        """
        Update the player's daily combo value

        :param value: (`int`)

        --

        :return: `None`
        """

        await self.__database.execute("""
                                      UPDATE player_time
                                      SET player_daily_combo = $1
                                      WHERE player_id = $2;
                                      """, [value, self.player.id])

        return

    async def update_hourly_time(self, value):
        """
        Update the value of the player hourly time

        :param value: (`int`)

        --

        :return: `None`
        """

        await self.__database.execute("""
                                      UPDATE player_time
                                      SET player_hourly_time = $1
                                      WHERE player_id = $2;
                                      """, [value, self.player.id])

        return

    async def update_daily_time(self, value):
        """
        Update the value of the player daily time

        :param value: (`int`)

        --

        :return: `None`
        """

        await self.__database.execute("""
                                      UPDATE player_time
                                      SET player_daily_time = $1
                                      WHERE player_id = $2;
                                      """, [value, self.player.id])

        return


class PlayerItem:

    def __init__(self, player):
        """
        :param player: (`Player`)
        """

        # Public
        self.player = player

        # Private
        self.__database = self.player.client.database

    # Public
    async def get_capsule(self, context):
        """
        Get the player's capsules

        :param context: (`discord.ext.commands.Context`)

        --

        :return: `list` of `Capsule` objects
        """

        # Init
        capsules = []
        player_capsule = await self.__database.fetch_row("""
                                                         SELECT *
                                                         FROM capsule
                                                         WHERE owner_id = $1;
                                                         """, [self.player.id])

        # If the player has capsules
        if player_capsule is not None:
            # Init
            capsule_ = None

            # Add the capsules objects to the capsules list
            for capsule in player_capsule:
                await asyncio.sleep(0)

                # Get capsule's info
                ref = capsule[1]
                unique_id = capsule[2]

                # Get the capsule object
                # Get normal capsule
                if ref is 0:
                    capsule_ = CapsuleN(context, self.player.client, self.player)

                    # Setup the capsule
                    capsule_.unique_id = unique_id

                # In the end, add the capsule to the list
                capsules.append(capsule_)

        return capsules
