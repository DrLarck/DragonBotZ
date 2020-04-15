"""
Represent a Normal capsule

--

Author : DrLarck

Last update : 15/04/20 by DrLarck
"""

# util
from utility.entity.capsule import Capsule
from utility.graphic.icon import GameIcon

# item
from utility.entity.item.training_item.sword_0 import Sword0


class CapsuleN(Capsule):

    def __init__(self, context, client, player):
        """
        :param context: (`discord.ext.commands.Context`)

        :param client: (`discord.ext.commands.Bot`)

        :param player: (`Player`)
        """

        # Inheritance
        Capsule.__init__(self, context, client, player)

        # Public
        self.reference = 0
        self.name = "Normal Capsule"
        self.icon = GameIcon().capsule_0

        # Rewards
        self.dragonstone = 5000
        self.zeni = 150000
        self.item = [Sword0]

        # Rates
        self.rate_item = 20
        self.rate_dragonstone = 50
        self.rate_zeni = 100
