"""Ability object (super class)

--

@author DrLarck

@update 18/07/20 by DrLarck"""

import asyncio
import random

from utility.graphic.icon import GameIcon


class Ability:

    def __init__(self, client):
        self.client  = client

        self.id          = 0
        self.name        = ""
        self.description = ""
        self.tooltip     = ""
        self.tooltip_set = False
        self.icon        = GameIcon().special_attack
        
        self.cost       = 0
        self.cooldown   = 0
        self.current_cd = 0

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

        self.ki_regen = 0

        self.apply_effect = []

        self.cleanse = False

    async def init(self, caster):
        """Init the ability

        --

        @return None"""

        if self.tooltip_set:
            return
            
        # Set the display of the ability's behaviour
        # for the ability tooltip
        ability_behaviour = ""

        if self.damage_direct > 0:
            # Get the highest stat
            highest = caster.damage.physical

            if caster.damage.ki > highest:
                highest = caster.damage.ki

            # Get the damage range
            direct_range = []
            highest_min  = int(highest * 0.9)

            direct_range.append(int((highest_min * self.damage_direct)/100))
            direct_range.append(int((highest * self.damage_direct)/100)) 

            # Set display
            ability_behaviour += f"\n__Damage__ :anger: : **{direct_range[0]:,}** - **{direct_range[1]:,}** direct damage"
        
        if self.damage_physical > 0:
            # Get the physical damage range
            physical_range = []
            phy_min        = await caster.damage.get_physical_min()
            phy_max        = caster.damage.physical

            physical_range.append(int((phy_min * self.damage_physical)/100))
            physical_range.append(int((phy_max * self.damage_physical)/100))

            ability_behaviour += f"\n__Damage__ :punch: : **{physical_range[0]:,}** - **{physical_range[1]:,}** physical damage"
        
        if self.damage_ki > 0:
            # Get the ki damage range
            ki_range = []
            ki_min   = await caster.damage.get_ki_min()
            ki_max   = caster.damage.ki

            ki_range.append(int((ki_min * self.damage_ki)/100))
            ki_range.append(int((ki_max * self.damage_ki)/100))

            ability_behaviour += f"\n__Damage__ :comet: : **{ki_range[0]:,}** - **{ki_range[1]:,}** ki damage"

        if self.ki_regen > 0:
            ability_behaviour += f"\n__Ki__ : **+ {self.ki_regen:,}** :fire:"
    
        if ability_behaviour != "":
            self.tooltip += ability_behaviour + '\n'

        self.tooltip_set = True

        return

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
            copy = Ability(self.client)

            # Configure the ability object, according to the 
            # fetched data
            data = data[0]

            # Ability info
            copy.name = data[1]

            if data[2] is not None:
                copy.description = data[2]
            
            if data[3] is not None:
                copy.tooltip = data[3]
            
            if data[4] is not None:
                copy.icon = data[4]
            
            # Ability condition
            copy.cost = data[5]
            copy.cooldown = data[6]

            copy.need_target = data[7]
            
            copy.target_ally = data[8]
            copy.target_enemy = data[9]

            copy.target_number = data[10]

            # Ability damage
            copy.damage_direct = data[11]
            copy.damage_physical = data[12]
            copy.damage_ki = data[13]

            # Ability heal
            copy.self_heal = data[14]

            copy.heal_direct = data[15]
            copy.heal_physical = data[16]
            copy.heal_ki = data[17]

            # Ability effect applying
            if data[18] is not None:
                effect_to_apply = data[18]

                # Get the list of effect id
                copy.apply_effect = effect_to_apply.split()

            # Cleansing info
            copy.cleanse = data[19]

            # Ability ki regen
            copy.ki_regen = data[20]

            return copy
        
        else:
            return None
        
    async def is_usable(self, caster):
        """Tells if the ability is usable or not and why

        --

        @return bool, str"""

        usable = True
        reason = ""

        # Check CD
        if self.current_cd > 0:
            usable = False
            reason = f"Ability on cooldown ! *({self.current_cd} ⌛)*"
        
        # Check cost
        elif caster.ki.current < self.cost:
            usable = False
            reason = f"Not enough ki ! *({caster.ki.current}/**{self.cost}** :fire:)*"

        return usable, reason
    
    async def use(self, caster, target):
        """Use the ability

        @param caster object Character

        @param target object Character

        --

        @return str"""
        
        display = ""

        if self.damage_direct > 0 or self.damage_physical > 0 or self.damage_ki > 0:
            # Damage the target
            damage = AbilityDamage(self, caster)

            display += await damage.inflict_damage(target)

        # Regen
        if self.ki_regen > 0:
            # The character gains an amount of ki between 90 % of the
            # ki regen up to 100 %
            ki_gain = random.randint(int(self.ki_regen*0.9), self.ki_regen)
            
            # Add the ki to the caster
            caster.ki.current += ki_gain
            await caster.ki.limit()

            # Set display for ki gain
            display += f"\n__Ki__ : **+ {ki_gain:,}** :fire:"

        # Set cd
        if self.cooldown > 0:
            self.current_cd = self.cooldown
        
        # Consum cost
        caster.ki.current -= self.cost
        await caster.ki.limit()

        return display


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
            
            # Random direct damage roll
            highest_stat = random.randint(int(highest_stat * 0.9), highest_stat)
            self.direct = int((self.ability.damage_direct * highest_stat) / 100)

        if self.ability.damage_physical > 0:
            # Physical damage calculation
            physical = random.randint(await self.caster.damage.get_physical_min(), self.caster.damage.physical)

            self.physical = int((self.ability.damage_physical * physical) / 100)
        
        if self.ability.damage_ki > 0:
            # Ki damage calculation
            ki = random.randint(await self.caster.damage.get_ki_min(), self.caster.damage.ki)

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

            damages.append(f"*- {self.direct:,}* 💢")
        
        if self.physical > 0:
            physical_reduction = 1 - (target.armor.floating / 100)

            physical_dealt = int(self.physical * physical_reduction)
            physical_dealt = int(physical_dealt - target.armor.fixed)

            if physical_dealt < 0:
                physical_dealt = 0

            target.health.current -= physical_dealt
            await target.health.limit()
            
            total_damage += physical_dealt

            damages.append(f"*- {physical_dealt:,}* :punch:")
        
        if self.ki > 0:
            ki_reduction = 1 - (target.spirit.floating / 100)

            ki_dealt = int(self.ki * ki_reduction)
            ki_dealt = int(ki_dealt - target.spirit.fixed)

            if ki_dealt < 0:
                ki_dealt = 0

            target.health.current -= ki_dealt
            await target.health.limit()
            
            total_damage += ki_dealt

            damages.append(f"*- {ki_dealt:,}* :comet:")

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
