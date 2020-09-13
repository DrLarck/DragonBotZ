"""Message input manager

--

@author DrLarck

@update 12/09/20 by DrLarck"""

import asyncio


class MessageInput:

    def __init__(self, client):
        self.client = client

    async def get_input(self, user):
        """Get the message input of a user

        @param Player user

        --

        @return str or None"""

        user_input = None

        # Check for the input
        def message_check(message):
            if message.author.id == user.id:
                return True

            else:
                return False

        # Get the message
        try:
            user_input = await self.client.wait_for(
                "message", check=message_check, timeout=60
            )

        except asyncio.TimeoutError:
            return None

        return user_input
