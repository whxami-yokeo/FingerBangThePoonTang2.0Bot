import asyncio
import discord
import logging
import os
import sys

from asyncio import sleep
from discord.ext import commands
from discord import Color
from print_color import print
from utils.EmbedGeneratorUtil import EmbedGenerator


class RestartCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="restart", help="Restarts the bot, safely!")
    async def restart(self, ctx: discord.ext.commands.Context):
        """
        Restarts the bot safely.
        :param ctx: This is the discord Interaction we can access data from
        :return:
        """

        embed = EmbedGenerator(self.bot).generate_title_message_embed_with_footer(title="Bot Restarting...",
                                                                                  description="Restarting, safely!",
                                                                                  colour=Color.magenta(),
                                                                                  timestamp=True)
        await ctx.reply(embed=embed, mention_author=False, ephemeral=True)

        print("Restarting...", tag="IN PROGRESS", tag_color="yellow", color="white")
        os.execv(sys.executable, ['python'] + sys.argv)


async def setup(bot: commands.Bot):
    await bot.add_cog(RestartCommand(bot))
