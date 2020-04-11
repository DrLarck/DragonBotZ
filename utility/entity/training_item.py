"""Represents a Training Item"""


class TrainingItem:

    def __init__(self, client, character):
        """:param character: (`Character`)

           :param client: (`discord.ext.commands.Bot`)"""

        # Public
        self.character = character
        self.reference = 0

        # Private
        self.__database = client.database

    # Public method
    async def apply_effect(self):
        """Apply the item's effects to the character
        
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
