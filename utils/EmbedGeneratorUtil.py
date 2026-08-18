import discord
from discord import Color
from discord.ext import commands


class EmbedGenerator(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def generate_simple_message_embed(description: str = commands.Parameter(name="description", description="The description of the embed you would like to make", kind=commands.Parameter.KEYWORD_ONLY),
                                      colour: discord.Color = commands.Parameter(name="colour", description="The colour of the embed you would like to make", kind=commands.Parameter.KEYWORD_ONLY),
                                      timestamp: bool = None):

        if description is None:
            raise commands.MissingRequiredArgument(
                param=commands.Parameter('description', commands.Parameter.KEYWORD_ONLY,
                                         description="The description of the embed you would like to make."))

        if colour is None:
            raise commands.MissingRequiredArgument(param=commands.Parameter('colour', commands.Parameter.KEYWORD_ONLY,
                                                                            description="The colour of the embed you would like to make."))

        embed = discord.Embed(description=description)
        embed.colour = colour

        if timestamp:
            embed.timestamp = discord.utils.utcnow()

        return embed

    def generate_simple_message_embed_with_footer(self, description: str = commands.Parameter(name="description", description="The description of the embed you would like to make", kind=commands.Parameter.KEYWORD_ONLY),
                                                  colour: discord.Color = commands.Parameter(name="colour", description="The colour of the embed you would like to make", kind=commands.Parameter.KEYWORD_ONLY),
                                                  timestamp: bool = False):

        if description is None:
            raise commands.MissingRequiredArgument(
                param=commands.Parameter('description', commands.Parameter.KEYWORD_ONLY,
                                         description="The description of the embed you would like to make."))

        if colour is None:
            raise commands.MissingRequiredArgument(param=commands.Parameter('colour', commands.Parameter.KEYWORD_ONLY,
                                                                            description="The colour of the embed you would like to make."))

        embed = discord.Embed(description=description)
        embed.colour = colour
        embed.set_footer(text=f"This message was brought to you by {self.bot.user.name}'s Message Delivery System!",
                         icon_url=self.bot.user.avatar.url)

        if timestamp:
            embed.timestamp = discord.utils.utcnow()

        return embed

    @staticmethod
    def generate_title_message_embed(title: str = commands.Parameter(name="title", description="The title of the embed you would like to make", kind=commands.Parameter.KEYWORD_ONLY),
                                     description: str = commands.Parameter(name="description", description="The description of the embed you would like to make", kind=commands.Parameter.KEYWORD_ONLY),
                                     colour: discord.Color = commands.Parameter(name="colour", description="The colour of the embed you would like to make", kind=commands.Parameter.KEYWORD_ONLY),
                                     timestamp: bool = False):

        if title is None:
            raise commands.MissingRequiredArgument(param=commands.Parameter('title', commands.Parameter.KEYWORD_ONLY,
                                                                            description="The title of the embed you would like to make."))

        if description is None:
            raise commands.MissingRequiredArgument(
                param=commands.Parameter('description', commands.Parameter.KEYWORD_ONLY,
                                         description="The description of the embed you would like to make."))

        if colour is None:
            raise commands.MissingRequiredArgument(param=commands.Parameter('colour', commands.Parameter.KEYWORD_ONLY,
                                                                            description="The colour of the embed you would like to make."))

        embed = discord.Embed(title=title, description=description)
        embed.colour = colour

        if timestamp:
            embed.timestamp = discord.utils.utcnow()

        return embed

    def generate_title_message_embed_with_footer(self, title: str = commands.Parameter(name="title", description="The title of the embed you would like to make", kind=commands.Parameter.KEYWORD_ONLY),
                                                 description: str = commands.Parameter(name="description", description="The description of the embed you would like to make", kind=commands.Parameter.KEYWORD_ONLY),
                                                 colour: discord.Color = commands.Parameter(name="colour", description="The colour of the embed you would like to make", kind=commands.Parameter.KEYWORD_ONLY),
                                                 timestamp: bool = False):

        if title is None:
            raise commands.MissingRequiredArgument(param=commands.Parameter('title', commands.Parameter.KEYWORD_ONLY,
                                                                            description="The title of the embed you would like to make."))

        if description is None:
            raise commands.MissingRequiredArgument(
                param=commands.Parameter('description', commands.Parameter.KEYWORD_ONLY,
                                         description="The description of the embed you would like to make."))

        if colour is None:
            raise commands.MissingRequiredArgument(param=commands.Parameter('colour', commands.Parameter.KEYWORD_ONLY,
                                                                            description="The colour of the embed you would like to make."))

        embed = discord.Embed(title=title, description=description)
        embed.colour = colour
        embed.set_footer(text=f"This message was brought to you by {self.bot.user.name}'s Message Delivery System!",
                         icon_url=self.bot.user.avatar.url)

        if timestamp:
            embed.timestamp = discord.utils.utcnow()

        return embed


async def setup(bot: commands.Bot):
    await bot.add_cog(EmbedGenerator(bot))
