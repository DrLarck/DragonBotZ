"""
Represent lv.1 Z-Sword

--

Author : DrLarck

Last update : 15/04/20 by DrLarck
"""

# util
from utility.entity.training_item import TrainingItem
from utility.graphic.icon import GameIcon


class Sword0(TrainingItem):

    def __init__(self, client):
        """
        :param client: (`discord.ext.commands.Bot`)
        """

        # Inheritance
        TrainingItem.__init__(self, client)

        # Public
        self.reference = 0
        self.name = "Z-Sword lv.1"
        self.icon = GameIcon().sword_0
