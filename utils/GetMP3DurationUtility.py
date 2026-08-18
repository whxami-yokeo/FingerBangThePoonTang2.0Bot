import os.path

from mutagen.mp3 import MP3
import discord
from discord.ext import commands
from pydub import AudioSegment
from pydub.silence import split_on_silence


class GeMP3DurationUtility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def get_mp3_duration(file_path: str = commands.Parameter(name="file_path",
                                                             description="The file path of the MP3 file you need to get the duration of",
                                                             kind=commands.Parameter.KEYWORD_ONLY)):

        if file_path is None:
            raise commands.MissingRequiredArgument(
                param=commands.Parameter('file_path', commands.Parameter.KEYWORD_ONLY,
                                         description="The file path of the MP3 file you need to get the duration of."))

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file located at: {file_path} does not exist.")

        try:
            audio = MP3(file_path)
            return audio.info.length
        except Exception as e:
            print(f"Error getting duration for {file_path}: {e}")
            return None

    @staticmethod
    def get_mp3_duration_sped_up(file_path: str = commands.Parameter(name="file_path",
                                                                     description="The file path of the MP3 file you need to get the duration of",
                                                                     kind=commands.Parameter.KEYWORD_ONLY)):

        if file_path is None:
            raise commands.MissingRequiredArgument(
                param=commands.Parameter('file_path', commands.Parameter.KEYWORD_ONLY,
                                         description="The file path of the MP3 file you need to get the duration of."))

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file located at: {file_path} does not exist.")

        try:
            audio = MP3(file_path)
            return audio.info.length / 1.5
        except Exception as e:
            print(f"Error getting duration for {file_path}: {e}")
            return None

    @staticmethod
    def trim_silence(input_file, output_file, silence_thresh=-80, min_silence_len=500):
        """
        Trims silence from the beginning and end of an audio file.

        Args:
            input_file (str): Path to the input audio file.
            Output_file (str): Path to save the trimmed audio file.
            Silence_thresh (int): dBFS value below which audio is considered silent.
            Min_silence_len (int): Minimum silence length in milliseconds to be considered when trimming.
            :param min_silence_len:
            :param silence_thresh:
            :param input_file:
            :param output_file:
        """
        audio = AudioSegment.from_file(input_file)
        chunks = split_on_silence(audio, silence_thresh=silence_thresh, min_silence_len=min_silence_len)

        # Concatenate the non-silent chunks back together
        trimmed_audio = sum(chunks, AudioSegment.silent(duration=0))
        trimmed_audio.export(output_file, format="mp3")  # You can change the format as needed

        return output_file


async def setup(bot: commands.Bot):
    await bot.add_cog(GeMP3DurationUtility(bot))
