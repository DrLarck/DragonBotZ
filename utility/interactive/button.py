"""
Button manager

--

Author : DrLarck

Last update : 07/04/20 by DrLarck
"""

import asyncio


class Button:

    def __init__(self, client, message):
        # Public
        self.client = client
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

    async def get_pressed(self, reaction, user):
        """
        Get the pressed button among the set of reaction that we want to track

        :param reaction: (`list` of `emote`)
        :param user: (`Player`)

        --

        :return: `str` or `None` (in case of timeout error)
        """

        # Init
        def check(_reaction, _user):
            if str(_reaction.emoji) in reaction and _user.id == user.id:
                return True

            else:
                return False

        try:
            reaction_, user_ = await self.client.wait_for("reaction_add",
                                                          timeout=60, check=check)

        except asyncio.TimeoutError:
            await self.message.clear_reactions()
            return None

        else:
            return str(reaction_.emoji)
