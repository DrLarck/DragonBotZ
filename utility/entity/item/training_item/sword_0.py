"""
Represent lv.1 Z-Sword

--

Author : DrLarck

Last update : 13/04/20 by DrLarck
"""

# util
from utility.entity.training_item import TrainingItem
from utility.graphic.icon import GameIcon


class Sword0(TrainingItem):

    def __init__(self, client, character=None):
        """
        :param client: (`discord.ext.commands.Bot`)

        :param character: (`Character`)
        """

        # Inheritance
        TrainingItem.__init__(self, client, character)

        # Public
        self.reference = 0
        self.name = "Z-Sword lv.1"
        self.icon = GameIcon().sword_0
