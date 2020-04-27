"""
Test ability
"""

# util
from utility.entity.ability import Ability


class Test(Ability):

    def __init__(self):
        Ability.__init__(self)

        self.id = 0
        self.name = "Test"
