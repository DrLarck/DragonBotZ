"""Ability object (super class)

--

@author DrLarck

@update 01/07/20 by DrLarck"""


class Ability:

    def __init__(self, client, context):
        self.client  = client
        self.context = context

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

        return
