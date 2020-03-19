"""
Custom embed

--

Author : DrLarck

Last update : 19/03/20 by DrLarck
"""

import discord


class CustomEmbed:

    @staticmethod
    async def setup(client, title="", description="", color=0,
                    footer="", thumbnail_url=""):
        """
        Setup the custom embed

        :param client: (`discord.ext.commands.Bot`)
        :param title: (`str`)
        :param description: (`str`)
        :param color: (`int`) Hexadecimal value
        :param footer: (`str`)
        :param thumbnail_url: (`str`) Valid url

        --

        :return: `discord.Embed`
        """

        # Init
        custom_embed = discord.Embed()
        avatar_url = client.user.avatar_url
        client_name = client.user.name

        # Setup the embed
        # In case the parameters have not been filled
        if not len(title) > 0:
            title = "No title provided"

        if not len(description) > 0:
            description = ""

        if not len(footer) > 0:
            footer = "Discord Ball Z : Origins | DrLarck & DrMegas | MIT License ©2019 - 2020"

        if not len(thumbnail_url) > 0:
            thumbnail_url = None

        if color == 0:  # If no color provided
            color = 0xF54719

        # Set the embed's attributes
        custom_embed.title = title
        custom_embed.description = description
        custom_embed.colour = color

        custom_embed.set_footer(text=footer, icon_url=avatar_url)
        custom_embed.set_author(name=client_name, icon_url=avatar_url)

        if thumbnail_url is not None:
            custom_embed.set_thumbnail(url=thumbnail_url)

        return custom_embed
