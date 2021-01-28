"""
Player object

--

Author : DrLarck

Last update : 28/01/21 by DrLarck
"""

import discord
import asyncio
import time

# util
from utility.entity.character import CharacterGetter

# items
from utility.entity.capsule import Capsule
from utility.entity.training_item import TrainingItem


class Player:

    def __init__(self, context, client, user):
        # Public
        self.context = context
        self.client = client
        self.name = user.name
        self.avatar = user.avatar_url
        self.id = user.id

        self.color  = 0xffffff
        self.circle = ""

        self.resource = PlayerResource(self)
        self.item = PlayerItem(self)
        self.experience = PlayerExperience(self)
        self.time = PlayerTime(self)

        self.combat = PlayerCombat(self)

    async def is_mod(self) -> bool:
        """Tells if the player is mod or not

        --

        @return `bool`"""

        data = await self.client.database.fetch_value(
            """
            SELECT player_id
            FROM mod
            WHERE player_id = $1;
            """, [self.id]
        )

        if data is not None:
            return True
        
        else:
            return False

    async def send_dm(self, message):
        """Send a DM to the user

        @param str message

        --

        @return None"""

        user = self.client.get_user(self.id)

        if user is not None:
            try:
                await user.send(message)

            except discord.Forbidden:
                print(f"Failed to DM {self.name} : Forbidden")
                pass

            except discord.HTTPException:
                print(f"Failed to DM {self.name} : Fail")
                pass

            else:
                pass

        return

    async def get_player_from_id(self, player_id):
        """Set the Player object according to the passed player_id

        @param int player_id

        --

        @return Player or None if not found"""

        # Retrieve the discord user
        user = await self.client.fetch_user(player_id)

        if user is not None:
            new_player = Player(self.context, self.client, user)
            return new_player

        else:
            return None

    async def get_premium_data(self):
        """Returns the player's premium info

        --

        @return dict : keys
        {'premium': bool, 'tier': int, 'total_month': int, 'until': int}"""

        # Init
        premium = False
        tier    = 0
        total   = 0

        data = await self.client.database.fetch_row("""
                                                    SELECT player_premium_until, player_premium_tier, player_premium_total_month
                                                    FROM player_info
                                                    WHERE player_id = $1;
                                                    """, [self.id])

        now = time.time()

        data = data[0]

        # If the player is premium
        if data[0] > now:
            premium = True

        remaining = int(data[0] - time.time())
        tier      = data[1]
        total     = data[2]

        # Make dict
        premium_data = {
            "premium": premium,
            "tier": tier,
            "total_month": total,
            "remaining": remaining
        }

        return premium_data

    async def is_registered(self):
        """Checks if the player is registered

        --

        @return bool"""

        registered = False

        # Check if the player is in the database
        data = await self.client.database.fetch_value(
            """
            SELECT player_name
            FROM player_info
            WHERE player_id = $1;
            """, [self.id]
        )

        if data is not None:
            registered = True

        return registered


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
                                                    SELECT player_dragonstone, player_zeni, player_dragonstone_shard
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
    
    async def get_dragonstone_shard(self):
        """Get the player's dragon stone shards amount 

        --

        @return `int`"""

        shards = await self.__database.fetch_value(
            """
            SELECT player_dragonstone_shard
            FROM player_resource
            WHERE player_id = $1
            """, [self.player.id]
        )

        return shards

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
    
    async def add_dragonstone_shard(self, amount):
        """Add an amount of dragon stone shards to the player's inventory

        @param double amount

        --

        @return None"""

        shards = await self.get_dragonstone_shard()

        shards += amount

        await self.__database.execute(
            """
            UPDATE player_resource
            SET player_dragonstone_shard = $1
            WHERE player_id = $2;
            """, [shards, self.player.id]
        )

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

        # Avoid negative value
        if dragonstone < 0:
            dragonstone = 0

        # Update the inventory
        await self.__database.execute("""
                                      UPDATE player_resource
                                      SET player_dragonstone = $1
                                      WHERE player_id = $2;
                                      """, [dragonstone, self.player.id])

        return
    
    async def remove_dragonstone_shard(self, amount):
        """Remove an amount of dragonstone shards to the player

        @param int amount

        --

        @return None"""

        shards = await self.get_dragonstone_shard()

        shards -= amount

        if shards < 0:
            shards = 0

        await self.__database.execute(
            """
            UPDATE player_resource
            SET player_dragonstone_shard = $1
            WHERE player_id = $2;
            """, [shards, self.player.id]
        )
        
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

        if zeni < 0:
            zeni = 0

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

    async def get_player_power(self):
        """Get the player's power points

        --

        @return int"""

        power = await self.__database.fetch_value("""
                                                  SELECT player_power
                                                  FROM player_info
                                                  WHERE player_id = $1;
                                                  """, [self.player.id])

        return power

    async def add_power(self, amount):
        """Add power points to the player's power

        @param int amount

        --

        @return None"""

        player_power = await self.get_player_power()

        if amount > 0:
            player_power += amount

            await self.__database.execute("""
                                          UPDATE player_info
                                          SET player_power = $1
                                          WHERE player_id = $2;
                                          """, [player_power, self.player.id])

        return

    async def remove_power(self, amount):
        """Remove power points to the player's power

        @param int amount

        --

        @return None"""

        player_power = await self.get_player_power()

        if amount > 0:
            player_power -= amount

            await self.__database.execute("""
                                          UPDATE player_info
                                          SET player_power = $1
                                          WHERE player_id = $2;
                                          """, [player_power, self.player.id])

        return


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
        self.__capsule = Capsule(self.player.context, self.player.client, self.player)
        self.__training_item = TrainingItem(self.player.client)

    # Public
    async def add_training_item(self, reference):
        """
        Add a training item into the player's inventory

        :param reference: (`int`)

        --

        :return: `None`
        """

        await self.__database.execute("""
                                      INSERT INTO training_item(training_item_reference, owner_id, owner_name)
                                      VALUES($1, $2, $3);
                                      """, [reference, self.player.id, self.player.name])

        await self.__training_item.set_unique_id()

        return

    async def add_capsule(self, rarity):
        """
        Add a capsule into the plaFyer's inventory

        :param rarity: (`int`)

        --

        :return: `None`
        """

        # Init
        if rarity < 0:
            rarity = 0

        elif rarity > 5:
            rarity = 5

        await self.__database.execute("""
                                      INSERT INTO capsule(capsule_reference, owner_id, owner_name)
                                      VALUES($1, $2, $3);
                                      """, [rarity, self.player.id, self.player.name])

        await self.__capsule.set_unique_id()

        return

    async def get_capsule(self):
        """
        Get the player's capsules

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
            capsule_ref = Capsule(self.player.context, self.player.client, self.player)

            # Add the capsules objects to the capsules list
            for capsule in player_capsule:
                await asyncio.sleep(0)

                # Get capsule's info
                ref = capsule[1]
                unique_id = capsule[2]

                # Get the capsule object
                capsule_ = await capsule_ref.get_capsule_by_reference(ref)

                if capsule_ is not None:
                    # Setup the capsule
                    capsule_.unique_id = unique_id

                    # In the end, add the capsule to the list
                    capsules.append(capsule_)

        return capsules

    async def get_capsule_by_rarity(self, rarity):
        """
        Return a list of capsule of the passed rarity

        :param rarity: (`int`)

        --

        :return: `list` of `Capsule`
        """

        # Init
        capsules = []
        player_capsule = await self.__database.fetch_row("""
                                                         SELECT *
                                                         FROM capsule
                                                         WHERE capsule_reference = $1 AND owner_id = $2;
                                                         """, [rarity, self.player.id])

        # If the player has capsules of the passed rarity
        if player_capsule is not None:
            # Get the capsule objects
            capsule_ref = Capsule(self.player.context, self.player.client, self.player)

            for capsule in player_capsule:
                await asyncio.sleep(0)
                # Get capsule info
                reference = capsule[1]
                unique_id = capsule[2]

                # Get the capsule object
                capsule_ = await capsule_ref.get_capsule_by_reference(reference)

                if capsule_ is not None:
                    # Setup the object
                    capsule_.unique_id = unique_id

                    # Add the capsule in the list
                    capsules.append(capsule_)

        return capsules

    async def open_capsule(self, rarity):
        """
        Open a random capsule of the rarity

        :param rarity: (`int`)

        --

        :return: `None`
        """

        # Get the player's capsule by rarity
        player_capsule = await self.get_capsule_by_rarity(rarity)

        # If the player has capsules
        if len(player_capsule) > 0:
            # Select a capsule to open
            capsule_to_open = player_capsule[0]

            # Open the capsule
            await capsule_to_open.open()

        return

    async def has_character(self, unique_id):
        """Return true if the player has the passed character

        @param str unique_id

        --

        @return bool"""

        has_it = False

        character = await self.__database.fetch_value("""
                                                      SELECT character_unique_id
                                                      FROM character_unique
                                                      WHERE character_owner_id = $1 AND character_unique_id = $2;
                                                      """, [self.player.id, unique_id])

        if character is not None:
            has_it = True

        return has_it


class PlayerCombat:

    def __init__(self, player):
        """
        :param player: (`Player`)
        """

        # Public
        self.player         = player
        self.team           = []
        self.unique_id_team = []

        # Private
        self.__database = self.player.client.database

    async def get_team(self):
        """
        Get the player's team

        --

        :return: `list` of `Character`
        """

        # Init
        team = []
        player_team = await self.__database.fetch_value("""
                                                        SELECT player_team
                                                        FROM player_combat
                                                        WHERE player_id = $1;
                                                        """, [self.player.id])

        player_team = player_team.split()
        self.unique_id_team = player_team

        # Check if the player has a team set up
        if len(player_team) > 0:
            char_getter = CharacterGetter()

            # Get the instance of each character
            count = 0
            for unique_id in player_team:
                await asyncio.sleep(0)

                character = await char_getter.get_from_unique(self.player.client, self.__database, unique_id)

                # If the character is not found, remove it from the team
                if character is None:
                    await self.remove_character(count, from_get_team=True)
                
                else:
                    # Add the character to the team list
                    team.append(character)
                
                count += 1

        self.team = team

        return team

    async def add_character(self, unique_id, tool_shop):
        """Add a character to the player's team

        @param str unique_id

        @param ToolShop tool_shop

        --

        @return bool, in case of false, return a reason str too"""

        reason = ""
        success = False
        getter = CharacterGetter()

        # Check if the character is on sale
        shop_tool = tool_shop
        on_sale = await shop_tool.find_character(unique_id)

        # Check if there is a character with the same reference
        # in the team
        duplicate = False
        exists = False

        await self.get_team()
        new_character = await getter.get_from_unique(
            self.player.client, self.__database, unique_id
        )

        # If the character exists
        if new_character is not None:
            exists = True

            for character in self.team:
                await asyncio.sleep(0)

                if character.id == new_character.id:
                    duplicate = True
                    break
        
        # Check if the player owns the character
        owns = await self.player.item.has_character(unique_id)

        # If duplicate, return false and the reason
        if duplicate:
            success = False
            reason = ":x: There is already a similar character in your team"

            return success, reason

        # If the team is full
        elif len(self.team) >= 3:
            success = False
            reason = ":x: Your team is full"

        elif on_sale:
            success = False
            reason = ":x: This character is currently on sale"

        elif not exists:
            success = False
            reason = f":x: Unable to find any character with `{unique_id}` as unique id"

        elif not owns:
            success = False
            reason = ":x: You do not own this character"

        # If everything is ok, add the character
        else:
            # Retrieve the player's team ids
            team_id = ""
            for unique in self.unique_id_team:
                await asyncio.sleep(0)

                team_id += f"{unique} "

            # Update the ids
            team_id += f"{unique_id} "

            # Update the database
            await self.__database.execute("""
                                          UPDATE player_combat
                                          SET player_team = $1
                                          WHERE player_id = $2;
                                          """, [team_id, self.player.id])

            # Lock the character to avoid the player to recycle it
            await self.__database.execute(
                """
                UPDATE character_unique
                SET locked = true
                WHERE character_unique_id = $1
                """, [unique_id]
            )

            success = True
            reason = f"You've added **{new_character.name}**{new_character.type.icon} lv.**{new_character.level}** in your team !"

        return success, reason

    async def get_fighter_slot_by_id(self, unique_id):
        """Return the character's slot index according to the unique_id

        @param str unique_id

        --

        @return int or None"""

        await self.get_team()

        slot = None

        # Check if the character is in the player's team
        is_in = False
        if unique_id in self.unique_id_team:
            is_in = True

        # Get the character's slot index
        if is_in:
            index = 0
            for character in self.unique_id_team:
                await asyncio.sleep(0)

                if character == unique_id:
                    slot = index
                    break

                index += 1

        return slot

    async def remove_character(self, slot, from_get_team=False):
        """Remove a character from the player's team

        --

        @return str"""

        reason = ""
        getter = CharacterGetter()

        # If remove_character() is not called by get_team()
        if not from_get_team:
            # Check if the character is in the player's team
            await self.get_team()

        # Get the unique id of the character
        unique_id = self.unique_id_team[slot]

        is_in = False
        for unique in self.unique_id_team:
            await asyncio.sleep(0)

            if unique == unique_id:
                is_in = True
                break

        if is_in:
            # Get the character
            character = await getter.get_from_unique(self.player.client, self.__database, unique_id)

            # Remove the character from the team
            # and get a new string to update the database
            self.unique_id_team.remove(unique_id)
            new_team = ""

            for unique in self.unique_id_team:
                await asyncio.sleep(0)

                new_team += unique + ' '

            await self.__database.execute("""
                                          UPDATE player_combat
                                          SET player_team = $1
                                          WHERE player_id = $2;
                                          """, [new_team, self.player.id])

            # Display this message if the call is not from get_team()
            if not from_get_team:
                reason = f"Successfully removed **{character.name}**{character.type.icon} from your team"

        else:
            reason = "This character is not in your team"

        return reason

    async def get_average_team_level(self):
        """Returns the average player's team level

        --

        @return int"""

        average_level = 0

        for character in self.team:
            await asyncio.sleep(0)

            average_level += character.level

        average_level = int(
            average_level / len(self.team)
        )

        return average_level
