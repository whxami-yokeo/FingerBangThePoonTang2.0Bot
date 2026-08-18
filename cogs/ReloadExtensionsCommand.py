import discord
from discord import Color
from discord.ext import commands
import os
from print_color import print


class ReloadExtensionsCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.successes = []
        self.fails = []

    # noinspection PyBroadException
    @commands.is_owner()
    @commands.command(name="reloadevents",
                      help="Reloads all events in the 'events' directory. Can only be used by bot owner.")
    async def reloadevents(self, ctx: discord.ext.commands.Context):
        """
        Reloads all events in the 'events' directory
        :param ctx: This is the discord Interaction we can access data from.
        :return:
        """

        print("Reloading Events...")
        for filename in os.listdir(f'{self.bot.location}/events/'):
            if filename.endswith('.py'):
                try:
                    await self.bot.reload_extension(f'events.{filename[:-3]}')
                    self.successes.append(filename[:-3])
                    print(f"Reloaded Event: {filename[:-3]}", tag="SUCCESS", tag_color="green", color="white")
                except Exception:
                    self.fails.append(filename[:-3])
                    print(f"Could Not Reload Event: {filename[:-3]}", tag="FAILURE", tag_color="red", color="red")

        embed = discord.Embed(title="Reload Events Command Has Been Ran")
        embed.colour = Color.magenta()
        embed.set_footer(
            text="Please reach out to bot support if one of the events has been unsuccessful for over 24 hours!",
            icon_url=self.bot.user.avatar.url)
        if len(self.successes):
            embed.add_field(name="Successfully Reloaded Events:", value="\n".join(self.successes))

        if len(self.fails):
            embed.add_field(name="Unsuccessful Reloaded Events:", value="\n".join(self.fails))

        await ctx.reply(embed=embed, mention_author=False, ephemeral=True)

        self.fails.clear()
        self.successes.clear()

    # noinspection PyBroadException
    @commands.is_owner()
    @commands.command(name="reloadcmds",
                      help="Reloads all commands in the 'commands' directory. Can only be used by bot owner.")
    async def reloadcmds(self, ctx: discord.ext.commands.Context):
        """
        Reloads all commands in the 'commands' directory
        :param ctx: This is the discord Interaction we can access data from.
        :return:
        """

        for filename in os.listdir(f'{self.bot.location}/cogs/'):
            if filename.endswith('.py'):
                try:
                    await self.bot.reload_extension(f'cogs.{filename[:-3]}')
                    self.successes.append(filename[:-3])
                    print(f"Reloaded Command: {filename[:-3]}", tag="SUCCESS", tag_color="green", color="white")
                except Exception:
                    self.fails.append(filename[:-3])
                    print(f"Reloaded Command: {filename[:-3]}", tag="FAILURE", tag_color="red", color="red")

        embed = discord.Embed(title="Reload Commands Command Has Been Ran")
        embed.colour = Color.magenta()
        embed.set_footer(
            text="Please reach out to bot support if one of the commands has been unsuccessful for over 24 hours!",
            icon_url=self.bot.user.avatar.url)
        if len(self.successes):
            embed.add_field(name="Successfully Reloaded Commands:", value="\n".join(self.successes))

        if len(self.fails):
            embed.add_field(name="Unsuccessful Reloaded Commands:", value="\n".join(self.fails))

        await ctx.reply(embed=embed, mention_author=False, ephemeral=True)

        self.fails.clear()
        self.successes.clear()

    # noinspection PyBroadException
    @commands.is_owner()
    @commands.command(name="reloadutils",
                      help="Reloads all utilities in the 'utils' directory. Can only be used by bot owner.")
    async def reloadutils(self, ctx: discord.ext.commands.Context):
        """
        Reloads all utilities in the 'utils' directory.
        :param ctx: This is the discord Interaction we can access data from.
        :return:
        """

        for filename in os.listdir(f'{self.bot.location}/utils/'):
            if filename.endswith('.py'):
                try:
                    await self.bot.reload_extension(f'utils.{filename[:-3]}')
                    self.successes.append(filename[:-3])
                    print(f"Reloaded Utility: {filename[:-3]}", tag="SUCCESS", tag_color="green", color="white")
                except Exception:
                    self.fails.append(filename[:-3])
                    print(f"Reloaded Utility: {filename[:-3]}", tag="FAILURE", tag_color="red", color="red")

        embed = discord.Embed(title="Reload Utilities Command Has Been Ran")
        embed.colour = Color.magenta()
        embed.set_footer(
            text="Please reach out to bot support if one of the utilities has been unsuccessful for over 24 hours!",
            icon_url=self.bot.user.avatar.url)
        if len(self.successes):
            embed.add_field(name="Successfully Reloaded Utilities:", value="\n".join(self.successes))

        if len(self.fails):
            embed.add_field(name="Unsuccessful Reloaded Utilities:", value="\n".join(self.fails))

        await ctx.reply(embed=embed, mention_author=False, ephemeral=True)

        self.fails.clear()
        self.successes.clear()

    # noinspection PyBroadException
    @commands.is_owner()
    @commands.command(name="reloadviews",
                      help="Reloads all views in the 'views' directory. Can only be used by bot owner.")
    async def reloadviews(self, ctx: discord.ext.commands.Context):
        """
        Reloads all views in the 'views' directory.
        :param ctx: This is the discord Interaction we can access data from.
        :return:
        """

        for filename in os.listdir(f'{self.bot.location}/utils/custom/views/'):
            if filename.endswith('.py'):
                try:
                    await self.bot.reload_extension(f'utils.custom.views.{filename[:-3]}')
                    self.successes.append(filename[:-3])
                    print(f"Reloaded View: {filename[:-3]}", tag="SUCCESS", tag_color="green", color="white")
                except Exception:
                    self.fails.append(filename[:-3])
                    print(f"Reloaded View: {filename[:-3]}", tag="FAILURE", tag_color="red", color="red")

        embed = discord.Embed(title="Reload Views Command Has Been Ran")
        embed.colour = Color.magenta()
        embed.set_footer(
            text="Please reach out to bot support if one of the views has been unsuccessful for over 24 hours!",
            icon_url=self.bot.user.avatar.url)
        if len(self.successes):
            embed.add_field(name="Successfully Reloaded Views:", value="\n".join(self.successes))

        if len(self.fails):
            embed.add_field(name="Unsuccessful Reloaded Views:", value="\n".join(self.fails))

        await ctx.reply(embed=embed, mention_author=False, ephemeral=True)

        self.fails.clear()
        self.successes.clear()

    @commands.is_owner()
    @commands.command(name="reloadall",
                      help="Reloads all views, utilities, events, and commands. Can only be used by bot owner.")
    async def reloadall(self, ctx: discord.ext.commands.Context):
        await self.reloadevents(ctx)
        await self.reloadcmds(ctx)
        await self.reloadutils(ctx)
        await self.reloadviews(ctx)


async def setup(bot: commands.Bot):
    await bot.add_cog(ReloadExtensionsCommand(bot))
