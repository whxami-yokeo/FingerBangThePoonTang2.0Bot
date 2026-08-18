import discord
from discord import Color
from discord.ext import commands

from utils.EmbedGeneratorUtil import EmbedGenerator


class OnError(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(self, ctx: discord.ext.commands.Context, error: discord.ext.commands.CommandError):
        """
        Runs if any of the bot errors are not already caught, throw an error.
        :param ctx: This is the discord Interaction we can access data from
        :param error: This is the error message that is thrown whenever the error is thrown.
        :return:
        """

        print(error)


async def setup(bot: commands.Bot):
    await bot.add_cog(OnError(bot))
