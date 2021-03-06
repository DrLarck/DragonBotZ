"""Represents a Training Item

--

Author : DrLarck

Last update: 15/04/20 by DrLarck"""

import asyncio

# tool
from utility.global_tool import GlobalTool


class TrainingItem:

    def __init__(self, client):
        """:param client: (`discord.ext.commands.Bot`)"""

        # Public
        self.client = client
        self.reference = 0

        # Info
        self.name = ""
        self.icon = ""

        # Private
        self.__database = client.database
        self.__global_tool = GlobalTool()

    # Public method
    async def apply_effect(self, character):
        """Apply the item's effects to the character

        :param character: (`Character`)
        
        --
        
        :return: `None`"""

        return
    
    async def get_from_unique(self, unique_id):
        """Get a training item reference from its unique id

        --

        :return: `int` or `None` if not found"""

        reference = await self.__database.fetch_val("""
                                                    SELECT reference 
                                                    FROM training_item
                                                    WHERE unique_id = $1;
                                                    """, [unique_id])
        
        return reference

    async def get_from_reference(self, reference):
        """
        Generate a training item according to the reference

        :param reference: (`int`)

        --

        :return: `TrainingItem` or `None`
        """

        # Init
        training_item = None

        if reference is 0:
            from utility.entity.item.training_item.sword_0 import Sword0
            training_item = Sword0(self.client)

        return training_item

    async def set_unique_id(self):
        """Generate an unique id for the training items that have 'NONE' as unique id

        --

        :return: `None`"""

        # Get the items that have 'NONE' as unique id
        items = await self.__database.fetch_row("""
                                                SELECT reference
                                                FROM training_item
                                                WHERE unique_id = 'NONE';
                                                """)

        # Generate a unique id for all those items
        for item in items:
            await asyncio.sleep(0)

            # Get the unique item's reference
            reference = item[0]
            unique_id = await self.__global_tool.generate_unique_id(reference)

            # Update the unique id
            await self.__database.execute("""
                                          UPDATE training_item
                                          SET unique_id = $1
                                          WHERE reference = $2;
                                          """, [unique_id, reference])

        return
