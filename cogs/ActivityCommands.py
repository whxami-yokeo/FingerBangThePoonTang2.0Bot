from csv import excel

import discord
from discord import Color
from discord.ext import commands
from discord.ext.commands import Parameter

from utils.EmbedGeneratorUtil import EmbedGenerator
from utils.enums.ActivityTypeEnum import ActivityOptions
from utils.custom.errors.FingerBangThePoonTangBotError import ActivityNotSupported


class SetActivityCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(name="setactivity", help="Sets The Current Activity Of The Bot!")
    async def setactivity(self, ctx: discord.ext.commands.Context,
                          activity_type: str = commands.Parameter(name="activity_type",
                                                                  description="The Type Of Activity. Listening, Watching, Streaming, Playing.",
                                                                  kind=commands.Parameter.KEYWORD_ONLY), *,
                          activity_name: str = commands.Parameter(name="activity_name",
                                                                  description="The Name Of The Activity You Would Like To Set.",
                                                                  kind=commands.Parameter.POSITIONAL_OR_KEYWORD)):
        """
        Sets the current activity of the bot!
        :param ctx: This is the discord Interaction we can access data from
        :param activity_type: The type of activity. Listening, watching, streaming, playing.
        :param activity_name: The name of the activity you would like to set.
        :return:
        """
        if activity_type is None:
            raise commands.MissingRequiredArgument(
                param=commands.Parameter('activity_type', commands.Parameter.KEYWORD_ONLY,
                                         description="The Type Of Activity. Listening, Watching, Streaming, Playing."))

        if activity_type.lower() not in ActivityOptions:
            raise ActivityNotSupported(error=f"You Input - {activity_type}")

        if activity_name is None:
            raise commands.MissingRequiredArgument(
                param=commands.Parameter('activity_name', commands.Parameter.POSITIONAL_OR_KEYWORD,
                                         description="The Name Of The Activity You Would Like To Set."))

        activity_name = activity_name.strip()
        activity = None

        if activity_type.lower() == ActivityOptions.PLAYING.value or activity_type.lower() == ActivityOptions.PLAYING.name:
            activity = discord.Game(name=activity_name)
        elif activity_type.lower() == ActivityOptions.STREAMING.value or activity_type.lower() == ActivityOptions.STREAMING.name:
            activity = discord.Streaming(name=activity_name, url="https://www.youtube.com")
        elif activity_type.lower() == ActivityOptions.LISTENING.value or activity_type.lower() == ActivityOptions.LISTENING.name:
            activity = discord.Activity(type=discord.ActivityType.listening, name=activity_name)
        elif activity_type.lower() == ActivityOptions.WATCHING.value or activity_type.lower() == ActivityOptions.WATCHING.name:
            activity = discord.Activity(type=discord.ActivityType.watching, name=activity_name)
        else:
            raise ActivityNotSupported(error=f"You Input - {activity_type}")

        if activity:
            await self.bot.change_presence(activity=activity)
            embed = EmbedGenerator(self.bot).generate_title_message_embed_with_footer(
                title="✅ Successfully Set Activity ✅",
                description=f"The Bot Has Successfully Changed Its Presence To The Following Activity: {activity.type.name} {activity.name}!",
                colour=Color.green(), timestamp=True)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed = EmbedGenerator(self.bot).generate_title_message_embed_with_footer(
                title="📛 An Error Has Occurred 📛",
                description="An Error Has Occurred Trying To Set The Activity. Please Try Again Or Reach Out To Support For Help!",
                colour=Color.red(), timestamp=True)
            await ctx.reply(embed=embed, ephemeral=True)

    @commands.is_owner()
    @commands.command(name="clearactivity", help="Clears The Current Activity From The Bot!!")
    async def clear_activity(self, ctx: discord.ext.commands.Context):
        """
        Clears the bot's current activity!
        :param ctx: This is the discord Interaction we can access data from
        :return:
        """

        try:
            await self.bot.change_presence(activity=None)
            embed = EmbedGenerator(self.bot).generate_title_message_embed_with_footer(
                title="✅ Successfully Cleared Activity ✅",
                description=f"The Bot Has Successfully Cleared Its Presence!", colour=Color.green(), timestamp=True)
            await ctx.reply(embed=embed, mention_author=False, ephemeral=True)
        except Exception as e:
            print(e)
            embed = EmbedGenerator(self.bot).generate_title_message_embed_with_footer(
                title="📛 An Error Has Occurred 📛",
                description=f"An Error Occurred While Trying To Set The Activity. Please Try Again Later Or Reach Out To Support For Help!!\n {e}",
                colour=Color.red(), timestamp=True)
            await ctx.reply(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(SetActivityCommand(bot))
