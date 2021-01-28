"""
Command checker

--

Author : DrLarck

Last update : 28/01/21 by DrLarck
"""

from discord.channel import DMChannel

# util
from utility.entity.player import Player
from utility.entity.combat import CombatGetter
from utility.command.tool.tool_trade import TradeGetter


class CommandChecker:

    # Public
    # Command checks
    @staticmethod
    async def game_ready(context):
        """
        Check if the game is ready

        :param context: (`discord.ext.commands.Context`)

        --

        :return: `bool`
        """

        # Init
        client = context.bot
        ready = client.is_ready()

        if not ready:
            await context.send("I'm currently booting up, please wait until the end of the process ...")
            return False
        
        else:
            return True

    @staticmethod
    async def no_dm(context):
        """
        Avoid the player to use the command in DM channel

        :param context: (`discord.ext.commands.Context`)

        --

        :return: `bool`
        """

        # Init
        message_channel = context.message.channel

        # If the channel is a DM channel
        if isinstance(message_channel, DMChannel):
            return False  # The command will be ignored

        # Not a DM channel
        else:
            return True

    @staticmethod
    async def can_register(context):
        """
        Check if the player is registered, if he's not registered, he can process the command

        :param context: (`discord.ext.commands.Context`)

        --

        :return: `bool`
        """

        # Init
        client = context.bot
        player = Player(context, client, context.message.author)
        database = client.database

        # Check if the player is in the database
        value = await database.fetch_value(f"SELECT player_name FROM player_info WHERE player_id = $1;", [player.id])

        # If the player is already registered
        # Send an error message telling him
        # That he is already registered
        if value is not None:
            await context.send(":x: You are already registered.")

            return False

        else:  # Allow the player to process the command if he is not registered
            return True

    @staticmethod
    async def register(context):
        """
        Check if the player is registered, if he is registered, he can process the command

        :param context: (`discord.ext.commands.Context`)

        --

        :return: `bool`
        """

        # Init
        client = context.bot
        player = Player(context, client, context.message.author)
        database = client.database

        # Check if the player is in the database
        value = await database.fetch_value(f"SELECT player_name FROM player_info WHERE player_id = $1;", [player.id])

        # If the player is registered
        # Return true
        if value is not None:
            return True

        else:  # The player is not registered
            await context.send(":x: You are not registered, to do so, use the `d!start` command.")

            return False

    @staticmethod
    async def not_fighting(context):
        """Check if the player is fighting or not

        @param context discord.ext.commands.Context

        --

        @return bool"""

        client        = context.bot
        combat_getter = CombatGetter()
        player        = Player(context, client, context.message.author)

        is_fighting = await combat_getter.player_is_fighting(player)

        if not is_fighting:
            return True

        else:
            await context.send(f":x: {player.name} You're already in a fight")
            return False

    @staticmethod
    async def has_team(context):
        """Check if the player has set up a team

        @param context discord.ext.commands.Context

        --

        @return bool"""

        client = context.bot
        player = Player(context, client, context.message.author)

        team = await player.combat.get_team()

        # Check if the player has set a team
        if len(team) > 0:
            return True

        else:
            return False

    @staticmethod
    async def not_trading(context):
        """Checks if the player is trading or not

        @param Context context

        --

        @return bool"""

        in_trade     = False
        trade_getter = TradeGetter()

        client = context.bot
        player = Player(context, client, context.message.author)

        in_trade = await trade_getter.is_trading(player)

        return not in_trade
    
    @staticmethod
    async def is_mod(context):
        """Check if the caller is mod

        @param context - `Context`

        --

        @return `bool`"""

        mod = False

        client = context.bot
        player = Player(context, client, context.message.author)

        mod = await player.is_mod()

        return mod
