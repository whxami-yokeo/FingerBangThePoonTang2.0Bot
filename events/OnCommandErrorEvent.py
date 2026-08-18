import logging

import discord
from discord import Color
from discord.ext import commands

from utils.EmbedGeneratorUtil import EmbedGenerator
from utils.custom.errors.FingerBangThePoonTangBotError import (
    BotAlreadyInChannelError,
)


class OnCommandError(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")

    @staticmethod
    def safe_error_text(error: Exception, max_length: int = 900) -> str:
        """
        Convert an exception to safe text for Discord.

        Discord limits embed descriptions and message content. More importantly,
        external libraries such as yt-dlp may attach enormous diagnostic output
        to exceptions, so never send unrestricted error text to Discord.
        """
        text = str(error).strip()

        if not text:
            text = "No error details were provided."

        # Prevent a raw exception from closing the Discord code block.
        text = text.replace("```", "'''")

        if len(text) > max_length:
            text = f"{text[:max_length]}..."

        return text

    async def send_error_embed(
            self,
            ctx: commands.Context,
            title: str,
            description: str,
    ):
        """
        Sends a regular command-context reply.

        Prefix-command Context.reply does not support ephemeral responses;
        `ephemeral=True` only applies to interaction responses/follow-ups.
        """
        description = description[:3500]

        embed = EmbedGenerator(
            self.bot
        ).generate_title_message_embed_with_footer(
            title=title,
            description=description,
            colour=Color.red(),
            timestamp=True,
        )

        await ctx.reply(embed=embed, mention_author=False)

    @commands.Cog.listener()
    async def on_command_error(
            self,
            ctx: commands.Context,
            error: commands.CommandError,
    ):
        """
        Handles uncaught prefix-command errors safely.
        """
        # Let a command-local error handler take responsibility if one exists.
        if ctx.command is not None and ctx.command.has_error_handler():
            return

        if isinstance(error, commands.NoPrivateMessage):
            embed = EmbedGenerator(
                self.bot
            ).generate_title_message_embed_with_footer(
                title="📛 An Error Has Occurred 📛",
                description="This command cannot be used in private messages.",
                colour=Color.red(),
                timestamp=True,
            )

            try:
                await ctx.author.send(embed=embed)
            except discord.Forbidden:
                pass

            return

        if isinstance(error, commands.MissingRole):
            await self.send_error_embed(
                ctx,
                "📛 An Error Has Occurred 📛",
                "You are missing the required role to perform this command.",
            )
            return

        if isinstance(error, commands.BotMissingRole):
            await self.send_error_embed(
                ctx,
                "📛 An Error Has Occurred 📛",
                "I am missing the required role to perform this command.",
            )
            return

        if isinstance(error, commands.MissingPermissions):
            await self.send_error_embed(
                ctx,
                "📛 An Error Has Occurred 📛",
                "You are missing the required permissions to perform this command.",
            )
            return

        if isinstance(error, commands.BotMissingPermissions):
            await self.send_error_embed(
                ctx,
                "📛 An Error Has Occurred 📛",
                "I am missing the required permissions to perform this command.",
            )
            return

        if isinstance(error, commands.CommandNotFound):
            await self.send_error_embed(
                ctx,
                "📛 An Error Has Occurred 📛",
                "That command does not exist. Please try again.",
            )
            return

        if isinstance(error, commands.MissingRequiredArgument):
            parameter_name = error.param.name
            parameter_description = error.param.description or "No description provided."

            await self.send_error_embed(
                ctx,
                "📛 An Error Has Occurred 📛",
                (
                    "You are missing a required argument.\n"
                    f"`{parameter_name}`: {parameter_description}"
                ),
            )
            return

        if isinstance(error, BotAlreadyInChannelError):
            await self.send_error_embed(
                ctx,
                "📛 A Command Error Has Occurred 📛",
                self.safe_error_text(error),
            )
            return

        if isinstance(error, commands.CommandInvokeError):
            original_error = getattr(error, "original", error)

            # Store the full traceback locally, not in Discord.
            self.logger.error(
                "Command %s failed: %s",
                ctx.command,
                original_error,
                exc_info=(
                    type(original_error),
                    original_error,
                    original_error.__traceback__,
                ),
            )

            # yt-dlp errors should be short and user-friendly. The detailed
            # message remains in your PyCharm console/log.
            if type(original_error).__name__ == "DownloadError":
                await self.send_error_embed(
                    ctx,
                    "📛 Song Download Failed 📛",
                    (
                        "I could not download that song. YouTube rejected or "
                        "temporarily failed the request.\n\n"
                        "Try again in a few minutes. If it keeps happening, "
                        "update yt-dlp and verify your browser-cookie and "
                        "JavaScript-runtime setup."
                    ),
                )
                return

            await self.send_error_embed(
                ctx,
                "📛 A Command Error Has Occurred 📛",
                (
                    f"Error type: `{type(original_error).__name__}`\n\n"
                    f"Details:\n```text\n"
                    f"{self.safe_error_text(original_error)}\n```"
                ),
            )
            return

        self.logger.error(
            "Unhandled command error in %s: %s",
            ctx.command,
            error,
            exc_info=(type(error), error, error.__traceback__),
        )

        await self.send_error_embed(
            ctx,
            "📛 An Unknown Error Has Occurred 📛",
            (
                f"Error type: `{type(error).__name__}`\n\n"
                f"Details:\n```text\n"
                f"{self.safe_error_text(error)}\n```"
            ),
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(OnCommandError(bot))
