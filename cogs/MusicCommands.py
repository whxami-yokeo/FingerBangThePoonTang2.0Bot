import asyncio
import logging
from typing import Optional

import discord
from discord import Color
from discord.ext import commands
from discord.utils import utcnow
from yt_dlp import YoutubeDL

from utils.EmbedGeneratorUtil import EmbedGenerator


class MusicCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")

        # Per-guild music state.
        self.vc: dict[int, Optional[discord.VoiceClient]] = {}
        self.music_queue: dict[int, list[dict]] = {}
        self.current_index: dict[int, int] = {}
        self.is_playing: dict[int, bool] = {}
        self.is_paused: dict[int, bool] = {}

        # Increments whenever a new audio track starts.
        # Used to invalidate an old delayed-disconnect task.
        self.playback_token: dict[int, int] = {}

    def ensure_guild_state(self, guild_id: int) -> None:
        """Create music state for a guild the first time it is used."""
        if guild_id not in self.vc:
            self.vc[guild_id] = None
            self.music_queue[guild_id] = []
            self.current_index[guild_id] = 0
            self.is_playing[guild_id] = False
            self.is_paused[guild_id] = False
            self.playback_token[guild_id] = 0

    async def set_streaming_presence(self, song: dict) -> None:
        """
        Show the active track as a Discord Streaming status.

        `link` is the YouTube webpage URL, not yt-dlp's temporary direct
        audio stream URL. The webpage URL is the one users should open.
        """
        title = song.get("title") or "Unknown title"
        url = song.get("link") or "https://www.youtube.com/"

        await self.bot.change_presence(
            activity=discord.Streaming(
                name=title,
                url=url,
            )
        )

    async def finish_queue(self, guild_id: int) -> None:
        """
        Wait briefly after the last track, then disconnect if nothing new
        started during the grace period.
        """
        self.ensure_guild_state(guild_id)

        token_at_finish = self.playback_token[guild_id]

        self.is_playing[guild_id] = False
        self.is_paused[guild_id] = False
        await self.bot.change_presence(activity=None)

        # Prevents the end of the final audio packet being cut off.
        await asyncio.sleep(4)

        # Another song started while waiting. Do not disconnect it.
        if self.playback_token[guild_id] != token_at_finish:
            return

        voice_client = self.vc[guild_id]

        self.music_queue[guild_id].clear()
        self.current_index[guild_id] = 0

        if voice_client is not None and voice_client.is_connected():
            try:
                await voice_client.disconnect()
            except discord.ClientException:
                self.logger.exception(
                    "Could not disconnect from voice in guild %s",
                    guild_id,
                )

        self.vc[guild_id] = None

    def now_playing_embed(
            self,
            ctx: commands.Context,
            song: dict,
    ) -> discord.Embed:
        embed = discord.Embed(
            title="▶️ Now Playing",
            description=f"[{song['title']}]({song['link']})",
            colour=Color.blue(),
            timestamp=utcnow(),
        )

        if song.get("thumbnail"):
            embed.set_thumbnail(url=song["thumbnail"])

        embed.add_field(
            name="Title",
            value=song["title"][:1024],
            inline=False,
        )
        embed.add_field(
            name="Channel",
            value=song.get("channel_url") or "Unknown",
            inline=True,
        )
        embed.add_field(
            name="Duration",
            value=song.get("duration_string") or "Unknown",
            inline=True,
        )
        embed.add_field(
            name="Added By",
            value=song.get("requester", "Unknown"),
            inline=True,
        )

        if self.bot.user:
            embed.set_footer(
                text=f"Requested through {self.bot.user.name}",
                icon_url=self.bot.user.display_avatar.url,
            )

        return embed

    async def join_vc(
            self,
            ctx: commands.Context,
            channel: discord.VoiceChannel,
    ) -> discord.VoiceClient:
        """
        Join the supplied voice channel or move there if needed.

        Uses ctx.guild.voice_client so a stale connection after a bot restart
        is detected instead of relying only on this Cog's in-memory state.
        """
        guild_id = ctx.guild.id
        self.ensure_guild_state(guild_id)

        voice_client = ctx.guild.voice_client

        if voice_client is None or not voice_client.is_connected():
            if voice_client is not None:
                try:
                    await voice_client.disconnect(force=True)
                except discord.ClientException:
                    pass

            self.vc[guild_id] = await channel.connect()

            # Gives a new voice connection time to become ready before FFmpeg
            # starts producing audio.
            await asyncio.sleep(1)

            return self.vc[guild_id]

        self.vc[guild_id] = voice_client

        if voice_client.channel != channel:
            await voice_client.move_to(channel)
            await asyncio.sleep(0.5)

        return voice_client

    def extract_yt(
            self,
            url: str,
            message: discord.Message,
            requester: str,
    ) -> Optional[dict]:
        """Extract a playable audio URL and video metadata with yt-dlp."""
        try:
            with YoutubeDL(self.bot.YDL_OPTS) as ydl:
                info = ydl.extract_info(url, download=False)

            if "entries" in info:
                info = info["entries"][0]

            return {
                # This is the permanent/watch-page URL for the Streaming
                # presence and the "Now Playing" embed.
                "link": info.get("webpage_url", url),

                # This is yt-dlp's temporary direct media URL for FFmpeg.
                "source": info["url"],

                "thumbnail": info.get("thumbnail"),
                "title": info.get("title", "Unknown title"),
                "description": info.get("description", ""),
                "duration_string": info.get("duration_string", "Unknown"),
                "like_count": info.get("like_count", "Unknown"),
                "view_count": info.get("view_count", "Unknown"),
                "channel_url": info.get("channel_url", "Unknown"),
                "message": message,
                "requester": requester,
            }

        except Exception:
            self.logger.exception("Could not extract YouTube information")
            return None

    def search_yt(self, search: str) -> str:
        """Return the webpage URL for the first YouTube search result."""
        with YoutubeDL(self.bot.YDL_OPTS) as ydl:
            results = ydl.extract_info(f"ytsearch1:{search}", download=False)
            return results["entries"][0]["webpage_url"]

    def after_song(
            self,
            ctx: commands.Context,
            error: Optional[Exception],
    ) -> None:
        """
        Called by Discord's audio thread after a track stops.

        The callback is not async, so schedule the work safely back on the
        main asyncio event loop.
        """
        if error:
            self.logger.error(
                "Player error in guild %s: %s",
                ctx.guild.id,
                error,
            )

        future = asyncio.run_coroutine_threadsafe(
            self.play_next(ctx),
            self.bot.loop,
        )

        try:
            future.result()
        except Exception:
            self.logger.exception("Unable to play next song")

    async def start_current_song(self, ctx: commands.Context) -> None:
        """Start the queue item at current_index without advancing it."""
        guild_id = ctx.guild.id
        self.ensure_guild_state(guild_id)

        queue = self.music_queue[guild_id]
        index = self.current_index[guild_id]

        if index >= len(queue):
            await self.finish_queue(guild_id)
            return

        song = queue[index]
        voice_client = self.vc[guild_id]

        if voice_client is None or not voice_client.is_connected():
            self.is_playing[guild_id] = False
            self.is_paused[guild_id] = False
            await self.bot.change_presence(activity=None)
            return

        if voice_client.is_playing() or voice_client.is_paused():
            voice_client.stop()

        self.is_playing[guild_id] = True
        self.is_paused[guild_id] = False

        embed = self.now_playing_embed(ctx, song)

        try:
            await song["message"].edit(embed=embed)
        except discord.HTTPException:
            self.logger.warning("Could not update the now-playing message")

        # This is the behavior you requested: every queued .play track is
        # shown as a Streaming activity with its title and YouTube page URL.
        await self.set_streaming_presence(song)

        source = discord.FFmpegPCMAudio(
            song["source"],
            executable="ffmpeg",
            **self.bot.FFMPEG_OPTS,
        )

        # Any delayed cleanup created for an earlier track is now obsolete.
        self.playback_token[guild_id] += 1

        voice_client.play(
            source,
            after=lambda error: self.after_song(ctx, error),
        )

    async def play_next(self, ctx: commands.Context) -> None:
        """Advance one item in the queue, or finish and disconnect."""
        guild_id = ctx.guild.id
        self.ensure_guild_state(guild_id)

        # `stop` and `leave` set this False before invoking VoiceClient.stop().
        # The after callback therefore cannot begin another queue item.
        if not self.is_playing[guild_id]:
            return

        self.current_index[guild_id] += 1

        if self.current_index[guild_id] >= len(self.music_queue[guild_id]):
            await self.finish_queue(guild_id)
            return

        await self.start_current_song(ctx)

    @commands.command(name="join", help="Joins your current voice channel.")
    async def join(self, ctx: commands.Context) -> None:
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.reply(
                "You need to join a voice channel first.",
                mention_author=False,
            )
            return

        await self.join_vc(ctx, ctx.author.voice.channel)

        embed = EmbedGenerator(self.bot).generate_simple_message_embed(
            description=f"Joined **{ctx.author.voice.channel.name}**.",
            colour=Color.green(),
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="leave", help="Leaves voice and clears the queue.")
    async def leave(self, ctx: commands.Context) -> None:
        guild_id = ctx.guild.id
        self.ensure_guild_state(guild_id)

        self.playback_token[guild_id] += 1

        voice_client = self.vc[guild_id] or ctx.guild.voice_client

        self.is_playing[guild_id] = False
        self.is_paused[guild_id] = False
        self.music_queue[guild_id].clear()
        self.current_index[guild_id] = 0

        if voice_client is not None and voice_client.is_connected():
            try:
                await voice_client.disconnect()
            except discord.ClientException:
                self.logger.exception(
                    "Could not disconnect from voice in guild %s",
                    guild_id,
                )

        self.vc[guild_id] = None
        await self.bot.change_presence(activity=None)

        embed = EmbedGenerator(self.bot).generate_simple_message_embed(
            description="Disconnected and cleared the queue.",
            colour=Color.green(),
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="play", help="Plays a YouTube search result or URL.")
    async def play(self, ctx: commands.Context, *, query: str) -> None:
        guild_id = ctx.guild.id
        self.ensure_guild_state(guild_id)

        if not ctx.author.voice or not ctx.author.voice.channel:
            embed = EmbedGenerator(self.bot).generate_simple_message_embed(
                description="You need to join a voice channel before playing music.",
                colour=Color.dark_orange(),
            )
            await ctx.reply(embed=embed, mention_author=False)
            return

        searching_embed = EmbedGenerator(self.bot).generate_simple_message_embed(
            description=f"Searching for `{query}`...",
            colour=Color.blurple(),
        )
        message = await ctx.reply(embed=searching_embed, mention_author=False)

        try:
            if query.startswith(("https://", "http://")):
                url = query
            else:
                url = await asyncio.to_thread(self.search_yt, query)

            song = await asyncio.to_thread(
                self.extract_yt,
                url,
                message,
                ctx.author.mention,
            )

        except Exception:
            self.logger.exception("Search failed")
            song = None

        if song is None:
            error_embed = EmbedGenerator(self.bot).generate_simple_message_embed(
                description=(
                    "I could not find or load that song. "
                    "Try a different search or URL."
                ),
                colour=Color.red(),
            )
            await message.edit(embed=error_embed)
            return

        await self.join_vc(ctx, ctx.author.voice.channel)

        self.music_queue[guild_id].append(song)

        if not self.is_playing[guild_id] and not self.is_paused[guild_id]:
            self.current_index[guild_id] = len(self.music_queue[guild_id]) - 1

            found_embed = EmbedGenerator(self.bot).generate_simple_message_embed(
                description=f"Found **{song['title']}**. Starting playback...",
                colour=Color.green(),
            )
            await message.edit(embed=found_embed)

            await self.start_current_song(ctx)
            return

        position = len(self.music_queue[guild_id]) - self.current_index[guild_id] - 1

        queued_embed = EmbedGenerator(self.bot).generate_simple_message_embed(
            description=(
                f"Added **{song['title']}** to the queue "
                f"at position **{position}**."
            ),
            colour=Color.green(),
        )
        await message.edit(embed=queued_embed)

    @commands.command(
        name="queue",
        aliases=["q"],
        help="Shows the current music queue.",
    )
    async def queue(self, ctx: commands.Context) -> None:
        guild_id = ctx.guild.id
        self.ensure_guild_state(guild_id)

        queue = self.music_queue[guild_id]
        index = self.current_index[guild_id]

        if not queue or index >= len(queue):
            embed = EmbedGenerator(self.bot).generate_simple_message_embed(
                description="The queue is empty.",
                colour=Color.dark_orange(),
            )
            await ctx.reply(embed=embed, mention_author=False)
            return

        current_song = queue[index]
        lines = [
            f"**Now playing:** [{current_song['title']}]({current_song['link']})"
        ]

        upcoming = queue[index + 1:index + 11]

        if upcoming:
            lines.append("")
            lines.append("**Up next:**")

            for number, song in enumerate(upcoming, start=1):
                lines.append(f"`{number}.` [{song['title']}]({song['link']})")
        else:
            lines.append("")
            lines.append("*There are no more songs queued.*")

        remaining_count = len(queue) - index - 1

        if remaining_count > 10:
            lines.append("")
            lines.append(f"*...and {remaining_count - 10} more song(s).*")

        embed = discord.Embed(
            title="🎵 Music Queue",
            description="\n".join(lines),
            colour=Color.blue(),
            timestamp=utcnow(),
        )

        await ctx.reply(embed=embed, mention_author=False)

    @commands.has_role("Bot Admin")
    @commands.command(name="pause", help="Pauses the current song.")
    async def pause(self, ctx: commands.Context) -> None:
        guild_id = ctx.guild.id
        self.ensure_guild_state(guild_id)

        voice_client = self.vc[guild_id] or ctx.guild.voice_client

        if voice_client is None or not voice_client.is_connected():
            await ctx.reply(
                "I am not connected to a voice channel.",
                mention_author=False,
            )
            return

        if not voice_client.is_playing():
            await ctx.reply(
                "Nothing is currently playing.",
                mention_author=False,
            )
            return

        voice_client.pause()
        self.is_playing[guild_id] = False
        self.is_paused[guild_id] = True

        embed = EmbedGenerator(self.bot).generate_simple_message_embed(
            description="Music paused.",
            colour=Color.green(),
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.has_role("Bot Admin")
    @commands.command(name="resume", help="Resumes paused music.")
    async def resume(self, ctx: commands.Context) -> None:
        guild_id = ctx.guild.id
        self.ensure_guild_state(guild_id)

        voice_client = self.vc[guild_id] or ctx.guild.voice_client

        if voice_client is None or not voice_client.is_connected():
            await ctx.reply(
                "I am not connected to a voice channel.",
                mention_author=False,
            )
            return

        if not voice_client.is_paused():
            await ctx.reply(
                "Music is not paused.",
                mention_author=False,
            )
            return

        queue = self.music_queue[guild_id]
        index = self.current_index[guild_id]

        if index < len(queue):
            await self.set_streaming_presence(queue[index])

        voice_client.resume()
        self.is_playing[guild_id] = True
        self.is_paused[guild_id] = False

        embed = EmbedGenerator(self.bot).generate_simple_message_embed(
            description="Music resumed.",
            colour=Color.green(),
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.has_role("Bot Admin")
    @commands.command(name="skip", help="Skips the current song.")
    async def skip(self, ctx: commands.Context) -> None:
        guild_id = ctx.guild.id
        self.ensure_guild_state(guild_id)

        voice_client = self.vc[guild_id] or ctx.guild.voice_client

        if voice_client is None or not voice_client.is_connected():
            await ctx.reply(
                "I am not connected to a voice channel.",
                mention_author=False,
            )
            return

        if not voice_client.is_playing() and not voice_client.is_paused():
            await ctx.reply(
                "Nothing is currently playing.",
                mention_author=False,
            )
            return

        self.is_playing[guild_id] = True
        self.is_paused[guild_id] = False
        voice_client.stop()

        embed = EmbedGenerator(self.bot).generate_simple_message_embed(
            description="Skipped the current song.",
            colour=Color.green(),
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.has_role("Bot Admin")
    @commands.command(name="stop", help="Stops music and clears the queue.")
    async def stop(self, ctx: commands.Context) -> None:
        guild_id = ctx.guild.id
        self.ensure_guild_state(guild_id)

        self.playback_token[guild_id] += 1

        voice_client = self.vc[guild_id] or ctx.guild.voice_client

        self.is_playing[guild_id] = False
        self.is_paused[guild_id] = False
        self.music_queue[guild_id].clear()
        self.current_index[guild_id] = 0

        if voice_client and (voice_client.is_playing() or voice_client.is_paused()):
            voice_client.stop()

        await self.bot.change_presence(activity=None)

        embed = EmbedGenerator(self.bot).generate_simple_message_embed(
            description="Stopped playback and cleared the queue.",
            colour=Color.green(),
        )
        await ctx.reply(embed=embed, mention_author=False)


async def setup(bot: commands.Bot):
    await bot.add_cog(MusicCommands(bot))
