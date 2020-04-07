"""
Button manager

--

Author : DrLarck

Last update : 07/04/20 by DrLarck
"""

import asyncio


class Button:

    def __init__(self, message):
        # Public
        self.message = message

    # Public
    async def add(self, reaction):
        """
        Add a set of reactions to the message

        :param reaction: (`list` of `emote`)

        --

        :return: `None`
        """

        # Add the reactions
        for emote in reaction:
            await asyncio.sleep(0)

            await self.message.add_reaction(emote)

        return
