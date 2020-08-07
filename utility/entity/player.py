"""
Player object

--

Author : DrLarck

Last update : 07/08/20 by DrLarck
"""

import asyncio

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
            for unique_id in player_team:
                await asyncio.sleep(0)

                character = await char_getter.get_from_unique(self.player.client, self.__database, unique_id)

                # Add the character to the team list
                team.append(character)

        self.team = team

        return team
    
    async def add_character(self, unique_id):
        """Add a character to the player's team

        --

        @return bool, in case of false, return a reason str too"""

        reason = ""
        success = False
        getter = CharacterGetter()

        await self.get_team()
        new_character = await getter.get_from_unique(self.player.client, self.__database, unique_id)

        # Check if there is a character with the same reference
        # in the team
        duplicate = False

        for character in self.team:
            await asyncio.sleep(0)

            if character.id == new_character.id:
                duplicate = True
                break
        
        # If duplicate, return false and the reason
        if duplicate:
            success = False
            reason = ":x: There is already a similar character in your team"

            return success, reason

        # If the team is full
        elif len(self.team) >= 3:
            success = False
            reason = ":x: Your team is full"

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

            success = True
            reason = f"You've added **{new_character.name}**{new_character.type.icon} lv.**{new_character.level}** in your team !"

            return success, reason
    
    async def remove_character(self, slot):
        """Remove a character from the player's team

        --

        @return str"""

        reason = ""
        getter = CharacterGetter()

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
