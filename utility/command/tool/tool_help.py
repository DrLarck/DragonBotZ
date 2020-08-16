"""Helper

--

@author DrLarck

@update 16/08/20 by DrLarck"""

import asyncio

# util
from utility.graphic.embed import CustomEmbed
from utility.interactive.button import Button


class Help:

    def __init__(self):
        self.name        = ""
        self.invoke      = ""
        self.description = ""
        self.subcommand  = []

# BOX HELP
class HelpBox(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Box"
        self.invoke = "box"
        self.description = "Displays your characters collection"
        self.subcommand = [SubBoxUnique()]


class SubBoxUnique(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Unique characters box"
        self.invoke = "box unique <reference>"
        self.description = "Displays the unique id of your characters according to the passed reference"


# DAILY HELP
class HelpDaily(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Daily"
        self.invoke = "daily"
        self.description = "Allows you to receive daily rewards.\nCome back many days in a row to earn more rewards"


# HELP HELP
class HelpHelp(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Help"
        self.invoke = "help"
        self.description = "Displays this message"


# HOURLY HELP
class HelpHourly(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Hourly"
        self.invoke = "hourly"
        self.description = "Allows you to receive hourly rewards.\nThe more you play, the more you get."


# HELP INVENTORY
class HelpInventory(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Inventory"
        self.invoke = "inventory"
        self.description = "Displays your inventory which contains your resources, items, etc."


# HELP MISSION
class HelpMission(Help):
    
    def __init__(self):
        Help.__init__(self)

        self.name = "Mission"
        self.invoke = "mission"
        self.description = "Displays the list of available missions"

        self.subcommand = [SubMissionStart()]


# Sub missions commands
class SubMissionStart(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Mission start"
        self.invoke = "mission start <index>"
        self.description = "Starts a mission, according to the passed index"


# HELP PROFILE
class HelpProfile(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Profile"
        self.invoke = "profile"
        self.description = "Displays your profile, which contains informations about you"


# HELP SHOP
class HelpShop(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Shop"
        self.invoke = "shop"
        self.description = "Displays shop help"

        self.subcommand = [SubShopCharacter(), SubShopSell()]


class SubShopCharacter(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Shop character"
        self.invoke = "shop character <reference>"
        self.description = "Displays the on sale characters according to the passed reference"


class SubShopSell(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Shop sell"
        self.invoke = "shop sell <character/item> <unique id> <price>"
        self.description = "Allows you to sell an object to other players through the shop"


class SubShopBuy(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Shop buy"
        self.invoke = "shop buy <character/item> <unique id>"
        self.description = "Allows you to buy an object from the shop"
    

# HELP START
class HelpStart(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Start"
        self.invoke = "start"
        self.description = "Allows you to start your adventure and registers you to the database"


# HELP STATUS
class HelpStatus(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Status"
        self.invoke = "status"
        self.description = "Displays the bot's status, such as latencies and shard informations"


# HELP SUMMON
class HelpSummon(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Summon"
        self.invoke = "summon"
        self.description = "Allows you to summon a character from a banner and adds it to your collection"

        self.subcommand = [SubSummonBanner()]


# Subsummon
class SubSummonBanner(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Summon banner"
        self.invoke = "summon <index>"
        self.description = "Allows you to summon a character from a banner according to passed the index "


# HELP TEAM
class HelpTeam(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Team"
        self.invoke = "team"
        self.description = "Displays your team of characters"

        self.subcommand = [SubTeamAdd(), SubTeamRemove()]


# Subteam
class SubTeamAdd(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Team add"
        self.invoke = "team add <unique id>"
        self.description = "Adds a character to your team according to the passed unique id, you can find the unique id of a character by using the `box unique` command"


class SubTeamRemove(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Team remove"
        self.invoke = "team remove <slot>"
        self.description = "Allows you to remove a character from your team according to the passed slot, slot names are `a/b/c`"


# HELP TRAIN
class HelpTrain(Help):

    def __init__(self):
        Help.__init__(self)

        self.name = "Train"
        self.invoke = "train"
        self.description = "Starts a combat against a random enemy to let you gain experience points to level up the characters within your team"


class ToolHelp:
    
    __commands         = [HelpBox(), HelpDaily(), HelpHelp(),
                          HelpHourly(), HelpInventory(), HelpMission(),
                          HelpProfile(), HelpShop(), HelpStart(), 
                          HelpStatus(), HelpSummon(), HelpTeam(), 
                          HelpTrain()]
    __total_page       = 0
    __display_per_page = 5
    
    def __init__(self, client, context, player):
        self.client  = client
        self.context = context
        self.player  = player
    

    async def help_manager(self, data=None):
        """Manages the help displaying

        @param[opt] list data

        --

        @return None"""

        if data is None:
            data = self.__commands
        
        else:
            # Display the command panel
            help_panel = await self.get_detailed_help_for(1, data)
            await self.context.send(embed=help_panel)

        if len(data) > 0:
            self.__total_page = int(
                ((len(data) - 1) / self.__display_per_page) + 1
            )
        
            # Display and manage the help pannel
            stop    = False
            page_id = 1
            while not stop:
                await asyncio.sleep(0)
                
                page = await self.get_help_page(page_id, data)

                current_page = await self.context.send(embed=page)

                button      = Button(self.client, current_page)
                help_button = await self.get_buttons(page_id)

                await button.add(help_button)

                pressed = await button.get_pressed(help_button, self.player)

                if pressed is not None:
                    if pressed == '❌':
                        await current_page.delete()
                        break
                
                    # Go back to the first page
                    elif pressed == '⏮':
                        page_id = 1

                    # Go to the previous page
                    elif pressed == '◀':
                        page_id -= 1

                    # Go to the next page
                    elif pressed == '▶':
                        page_id += 1

                    # Go to the last page
                    elif pressed == '⏭':
                        page_id = self.__total_page
                    
                    # Delete to open a new one
                    await current_page.delete()
                
                else:
                    break
            
            else:
                await self.context.send(":x: Help panel is not available")

        return
    
    async def get_help_page(self, page, data):
        """Return the embed help page

        @param int page

        @param list data

        --

        @return discord.Embed"""

        help_page = await CustomEmbed().setup(
            self.client, title="Help panel", 
            description=f"Page {page}/{self.__total_page}\nUse `help <command>` to display detailed help"
        )

        start = (page - 1) * self.__display_per_page
        end   = page * self.__display_per_page

        if end > len(data):
            end = len(data)
        
        for i in range(start, end):
            await asyncio.sleep(0)

            current = data[i]

            help_page.add_field(
                name=current.invoke,
                value=current.description,
                inline=False
            )
        
        return help_page
    
    async def get_buttons(self, page):
        """Returns a set of buttons according to the page number

        @param int page

        --

        @return str list"""

        button_set = ['❌']

        if page > 1:
            button_set.append('⏮')
            button_set.append('◀')
        
        if page < self.__total_page:
            button_set.append('▶')
            button_set.append('⏭')

        return button_set
    
    async def get_detailed_help_for(self, page, command_name):
        """Returns the detailed help for the passed command

        @param int page

        @param str command_name

        --

        @return discord.Embed or None if not found"""

        exists = False

        # Look for the command
        for command in self.__commands:
            await asyncio.sleep(0)

            if command.name.lower() == command_name.lower():
                exists = True
                looked_command = command
                break
        
        if exists:
            command_page = await CustomEmbed().setup(
                self.client, title=f"{looked_command.name} help panel"
            )

            # Add the command to the panel
            command_page.add_field(
                name=looked_command.invoke,
                value=looked_command.description,
                inline=False
            )

            # Retrieve the subcommands
            for sub in looked_command.subcommand:
                await asyncio.sleep(0)

                command_page.add_field(
                    name=sub.invoke,
                    value=sub.description,
                    inline=False
                )
            
            return command_page
        
        else:
            return None
