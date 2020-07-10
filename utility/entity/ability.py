"""Ability object (super class)

--

@author DrLarck

@update 10/07/20 by DrLarck"""


class Ability:

    def __init__(self, client):
        self.client  = client

        self.id          = 0
        self.name        = ""
        self.description = ""
        self.tooltip     = ""
        self.icon        = ""
        
        self.cost     = 0
        self.cooldown = 0

        self.need_target   = False
        self.target_ally   = False
        self.target_enemy  = False
        self.target_number = 0

        self.damage_direct   = 0
        self.damage_physical = 0
        self.damage_ki       = 0

        self.self_heal     = False
        self.heal_direct   = 0
        self.heal_physical = 0
        self.heal_ki       = 0

        self.apply_effect = []

        self.cleanse = False

    async def get_ability_data(self, ability_id):
        """Get the ability data from the database
        
        :param ability_id: `int`
        
        --
        
        @return object Ability"""

        # Retrieve ability data
        data = await self.client.database.fetch_row("""
                                                    SELECT *
                                                    FROM character_ability
                                                    WHERE reference = $1;
                                                    """, [ability_id])

        if len(data) > 0:
            # Configure the ability object, according to the 
            # fetched data
            data = data[0]

            # Ability info
            self.name = data[1]

            if data[1] is not None:
                self.description = data[2]
            
            if data[2] is not None:
                self.tooltip = data[3]
            
            if data[3] is not None:
                self.icon = data[4]
            
            # Ability condition
            self.cost = data[5]
            self.cooldown = data[6]

            self.need_target = data[7]
            
            self.target_ally = data[8]
            self.target_enemy = data[9]

            self.target_number = data[10]

            # Ability damage
            self.damage_direct = data[11]
            self.damage_physical = data[12]
            self.damage_ki = data[13]

            # Ability heal
            self.self_heal = data[14]

            self.heal_direct = data[15]
            self.heal_physical = data[16]
            self.heal_ki = data[17]

            # Ability effect applying
            effect_to_apply = data[18]

            # Get the list of effect id
            self.apply_effect = effect_to_apply.split(" ")

            # Cleansing info
            self.cleanse = data[19]

            return self
        
        else:
            return None
