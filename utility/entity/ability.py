"""Ability object (super class)

--

@author DrLarck

@update 13/07/20 by DrLarck"""

import asyncio


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
            if data[18] is not None:
                effect_to_apply = data[18]

                # Get the list of effect id
                self.apply_effect = effect_to_apply.split()

            # Cleansing info
            self.cleanse = data[19]

            return self
        
        else:
            return None


class AbilityDamage:

    def __init__(self, ability, caster):
        self.ability = ability
        self.caster  = caster

        self.direct   = 0
        self.physical = 0
        self.ki       = 0

        self.heal = 0

    async def calculate_damage(self):
        """Calculate the damage/heal that the ability
        is going to deal/provide

        --

        @return object AbilityDamage"""

        if self.ability.damage_direct > 0:
            # Direct damage calculation
            # Check for the caster's stats, the direct damage
            # are based on the highest character's stat (phy, ki)
            highest_stat = 0
            if self.caster.damage.physical > self.caster.damage.ki:
                highest_stat = self.caster.damage.physical
            else:
                highest_stat = self.caster.damage.ki
            
            self.direct = int((self.ability.damage_direct * highest_stat) / 100)

        if self.ability.damage_physical > 0:
            # Physical damage calculation
            physical = self.caster.damage.physical

            self.physical = int((self.ability.damage_physical * physical) / 100)
        
        if self.ability.damage_ki > 0:
            # Ki damage calculation
            ki = self.caster.damage.Ki

            self.ki = int((self.ability.damage_ki * ki) / 100)

        return self

    async def inflict_damage(self, target):
        """Inflict the damage to the target

        --

        @return str"""
        
        # Get the damage
        await self.calculate_damage()

        display      = "__Damage__ : "
        total_damage = 0
        damages      = []

        if self.direct > 0:
            # Inflict the damage
            target.health.current -= self.direct
            await target.health.limit()

            total_damage += self.direct

            damages.append(f"*{self.direct:,}*💢")
        
        if self.physical > 0:
            physical_reduction = 1 - (target.armor.floating / 100)

            physical_dealt = int(self.physical * physical_reduction)
            physical_dealt = int(physical_dealt - target.armor.fixed)

            if physical_dealt < 0:
                physical_dealt = 0

            target.health.current -= physical_dealt
            await target.health.limit()
            
            total_damage += physical_dealt

            damages.append(f"*{physical_dealt}*:punch:")
        
        if self.ki > 0:
            ki_reduction = 1 - (target.spirit.floating / 100)

            ki_dealt = int(self.ki * ki_reduction)
            ki_dealt = int(ki_dealt - target.spirit.fixed)

            if ki_dealt < 0:
                ki_dealt = 0

            target.health.current -= ki_dealt
            await target.health.limit()
            
            total_damage += ki_dealt

            damages.append(f"*{physical_dealt}*:comet:")

        # Set the display
        display += f"**- {total_damage:,}** ("

        details = len(damages)
        index = 0
        for damage in damages:
            await asyncio.sleep(0)

            display += f"{damage}"

            # Add a separator if we didn't finish iterate the 
            # list
            if index < details - 1:
                display += " | "

            index += 1
        
        display += ")"

        return display
