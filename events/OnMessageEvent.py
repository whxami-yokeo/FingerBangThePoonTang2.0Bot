import discord
from discord import Color
from discord.ext import commands

from db_services.MysqlServices import check_if_user_exists_in_db, add_user_to_db, get_banned_words_from_db
from utils.EmbedGeneratorUtil import EmbedGenerator
from utils.custom.CustomDiscordUtils import get_channel_by_name
from utils.enums.ReasonsForDeletionEnum import DeletionReasons


class OnMessage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Runs for every message sent in any server. Can check messages for anything before processing them for commands.
        :param message: This is the message sent in any guild.
        :return:
        """
        if message.author == self.bot.user:
            return

        is_in_db = await check_if_user_exists_in_db(user_id=str(message.author.id), host=self.bot.db_host, user=self.bot.db_user, password=self.bot.db_pass, database=self.bot.db_db_name)
        if is_in_db:
            if not await add_user_to_db(user_id=str(message.author.id), name=message.author.name, host=self.bot.db_host, user=self.bot.db_user, password=self.bot.db_pass, database=self.bot.db_db_name):
                embed = EmbedGenerator(self.bot).generate_title_message_embed_with_footer(title="📛 An Error Has Occurred 📛", description="There has been an error adding the user to the database! Please reach out to support or try again later!", colour=Color.red(), timestamp=True)
                await message.channel.send(embed=embed, mention_author=True)

        banned_words = await get_banned_words_from_db(host=self.bot.db_host, user=self.bot.db_user, password=self.bot.db_pass, database=self.bot.db_db_name)
        result = any(item in message.content.lower() for (item, ) in banned_words)

        if result:
            embed1 = EmbedGenerator(self.bot).generate_simple_message_embed(description=f"{message.author.mention}, you may not use that word here!", colour=Color.dark_red(), timestamp=True)
            await message.channel.send(embed=embed1)

            log_channel = await get_channel_by_name(message.guild, "logs") or None

            if log_channel is None:
                raise commands.ChannelNotFound(argument=f"The channel with the name 'logs' could not be found in this guild.")

            embed = discord.Embed(title="📛 OnMessageErrorEvent / Message Automatically Deleted 📛", colour=Color.dark_red())
            embed.add_field(name="Author", value=message.author.mention, inline=True).add_field(name="Channel", value=message.channel.mention, inline=True)
            if message.content:
                embed.add_field(name="Content", value=message.content, inline=True)
            else:
                embed.add_field(name="Content", value="*(No content or embed/attachment only)*", inline=True)
            embed.add_field(name="Message ID", value=message.id, inline=True)
            embed.add_field(name="Deleted By", value=self.bot.user.mention, inline=True)
            embed.add_field(name="Reason For Deletion", value=DeletionReasons.BANNED_LANGUAGE, inline=True)
            embed.set_footer(text=f"This message was brought to you by {self.bot.user.name}'s Message Delivery System!", icon_url=self.bot.user.avatar.url)
            await message.delete()
            await log_channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(OnMessage(bot))
