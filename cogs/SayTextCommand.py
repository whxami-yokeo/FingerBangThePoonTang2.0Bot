import discord
from discord import Color
from discord.ext import commands
from ffmpeg.video import playback_speed
from gtts import gTTS
import asyncio
from deep_translator import GoogleTranslator
import os

from gtts.tts import Speed
from pydub import AudioSegment

from cogs.JoinCommand import JoinCommand
from cogs.LeaveCommand import LeaveCommand
from utils.EmbedGeneratorUtil import EmbedGenerator
from utils.GetMP3DurationUtility import GeMP3DurationUtility
from utils.custom.errors.FingerBangThePoonTangBotError import LanguageNotSupported
from utils.enums.LanguageEnum import Languages


class SayTextCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="saytext",
                      help="Turns the given message into an audio file, the bot will then join the current author's voice channel, and play the audio file then disconnect.")
    async def saytext(self, ctx: discord.ext.commands.Context,
                      language: str = commands.Parameter(name="language",
                                                         description="The language in which you would like the message spoken in",
                                                         kind=commands.Parameter.KEYWORD_ONLY),
                      *, msg: str = commands.Parameter(name="msg",
                                                       description="The message you would like to be spoken to you in a voice channel",
                                                       kind=commands.Parameter.POSITIONAL_OR_KEYWORD)):
        """
        Turns the given message into an audio file, the bot will then join the current author's voice channel, and play the audio file then disconnect.
        :param ctx: This is the discord Interaction we can access data from.
        :param language: The language in which you would like the message spoken in.
        :param msg: The message you would like to be spoken to you in a voice channel.
        :return:
        """

        if language is None:
            raise commands.MissingRequiredArgument(param=commands.Parameter('language', commands.Parameter.KEYWORD_ONLY,
                                                                            description=f"The language in which you would like the message spoken in"))

        if language.lower() not in Languages:
            raise LanguageNotSupported(message="The only supported languages are English and Spanish!",
                                       error=f"You input: {language}")

        if msg is None:
            raise commands.MissingRequiredArgument(
                param=commands.Parameter('msg', commands.Parameter.POSITIONAL_OR_KEYWORD,
                                         description="The message you would like to be spoken to you in a voice channel."))

        if not await JoinCommand.join_1(JoinCommand(self.bot), ctx):
            return

        embed = EmbedGenerator.generate_simple_message_embed(description=f"Now Converting Message to Speech!",
                                                             colour=Color.blurple())
        msg_ = await ctx.reply(embed=embed, mention_author=False)

        file_path = f"{self.bot.location}/utils/voice_files/{ctx.guild.id}-output.mp3"
        print(file_path)

        if language.lower() == Languages.ENGLISH.value:
            # tts = gTTS(msg, lang="en", tld="ie")
            tts = gTTS(msg, lang="en", tld="co.za")
            tts.save(file_path)
            GeMP3DurationUtility.trim_silence(input_file=file_path, output_file=file_path)
        elif language.lower() == Languages.SPANISH.value:
            translated_text = GoogleTranslator(source="en", target="es").translate(msg)
            tts = gTTS(translated_text, lang="es", tld="us")
            tts.save(file_path)
        elif language.lower() == Languages.FRENCH.value:
            translated_text = GoogleTranslator(source="en", target="fr").translate(msg)
            tts = gTTS(translated_text, lang="fr", tld="ca")
            tts.save(file_path)

        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        duration_seconds = GeMP3DurationUtility.get_mp3_duration_sped_up(file_path)

        if voice_client and voice_client.is_connected():
            if voice_client.is_playing():
                voice_client.stop_playing()

            ffmpeg_options = {
                'options': '-filter:a "atempo=1.5" -b:a 192k',
            }

            source = discord.FFmpegPCMAudio(source=file_path,
                                            **ffmpeg_options)
            embed1 = EmbedGenerator.generate_simple_message_embed(description=f"Now Speaking: {msg}",
                                                                  colour=Color.magenta())
            msg2 = await msg_.edit(embed=embed1)
            voice_client.play(source, after=lambda e: print(f"Player error: {e}") if e else None)

            while ctx.guild.voice_client.is_playing():
                await asyncio.sleep(duration_seconds + 1)

            embed2 = EmbedGenerator.generate_simple_message_embed(description=f"Finished Speaking!",
                                                                  colour=Color.green())
            await msg2.edit(embed=embed2)
            os.remove(file_path)
            await LeaveCommand.leave_1(LeaveCommand(self.bot), ctx)


async def setup(bot: commands.Bot):
    await bot.add_cog(SayTextCommand(bot))
