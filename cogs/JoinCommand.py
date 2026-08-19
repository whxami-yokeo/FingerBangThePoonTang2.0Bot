import discord
from discord.ext import commands

from utils.custom.errors.FingerBangThePoonTangBotError import (
    UserNotInChannelError,
    BotAlreadyInChannelError,
)


class JoinCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def join_member_voice(self, member: discord.Member) -> bool:
        """
        Connect the bot to the supplied member's current voice channel.

        Returns:
            True when the bot is connected to the member's voice channel.

        Raises:
            UserNotInChannelError: The member is not in voice.
            BotAlreadyInChannelError: The bot is in a different voice channel.
        """
        if member.voice is None or member.voice.channel is None:
            raise UserNotInChannelError(
                error="The Bot Cannot Join Your Channel Because You Are Not In One!"
            )

        target_channel = member.voice.channel
        voice_client = member.guild.voice_client

        # The bot is not currently connected in this server.
        if voice_client is None or not voice_client.is_connected():
            await target_channel.connect()
            return True

        # The bot is already in the same channel as the member.
        if voice_client.channel == target_channel:
            return True

        # Preserve your existing behavior: do not silently move the bot
        # from another channel when someone clicks the music button.
        raise BotAlreadyInChannelError(
            error=(
                "I Am Already In Another Voice Channel. "
                "Move me to your channel before trying to play this song."
            )
        )

    @commands.guild_only()
    @commands.has_role("Bot Admin")
    @commands.command(
        name="j",
        help="Joins The Bot To The Author's Voice Channel, If There Is One",
    )
    async def join_1(self, ctx: commands.Context):
        """
        Joins the bot to the command author's current voice channel.
        """
        try:
            await self.join_member_voice(ctx.author)

        except UserNotInChannelError:
            raise UserNotInChannelError(
                error="The Bot Cannot Join Your Channel Because You Are Not In One!"
            )

        except BotAlreadyInChannelError:
            raise BotAlreadyInChannelError(
                error=(
                    "I Am Already In Another Voice Channel. "
                    "Move me to your channel before trying to play this song."
                )
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(JoinCommand(bot))
