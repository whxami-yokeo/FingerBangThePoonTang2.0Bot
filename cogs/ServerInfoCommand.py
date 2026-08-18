import discord
from discord import Color
from discord.ext import commands

from utils.EmbedGeneratorUtil import EmbedGenerator


class ServerInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(name="si", help="Sends an embed to the current channel with information about the server")
    async def si(self, ctx: discord.ext.commands.Context):
        """
        Sends an embed to the current channel with information about the server.
        :param ctx: This is the discord Interaction we can access data from
        :return:
        """

        guild = ctx.author.guild
        embed = discord.Embed(
            colour=Color.light_embed(),
            title="Server Info",
            description="This command displays information about the server."
        )

        embed.add_field(name="Name", value=guild.name)
        embed.add_field(name="Description", value=guild.description)
        embed.add_field(name="ID", value=guild.id)
        embed.add_field(name="Owner", value=guild.owner)
        embed.add_field(name="Owner ID", value=guild.owner_id)
        embed.add_field(name="Guild Created At", value=guild.created_at)
        embed.add_field(name="Preferred Locale", value=guild.preferred_locale)
        embed.add_field(name="Explicit Content Filter", value=guild.explicit_content_filter)
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="AFK Channel", value=guild.afk_channel)
        embed.add_field(name="Public Updates Channel", value=guild.public_updates_channel)
        embed.add_field(name="Safety Alerts", value=guild.safety_alerts_channel)
        embed.add_field(name="Rules Channel", value=guild.rules_channel)
        embed.add_field(name="System Channel", value=guild.system_channel)
        embed.add_field(name="Verification Level", value=guild.verification_level)
        embed.add_field(name="MFA Level", value=guild.mfa_level)
        embed.set_footer(text=f"This message was brought to you by {self.bot.user.name}'s Message Delivery System!", icon_url=self.bot.user.avatar.url)
        embed.set_thumbnail(url=guild.icon)
        embed.timestamp = discord.utils.utcnow()

        await ctx.reply(embed=embed, mention_author=False)


async def setup(bot: commands.Bot):
    await bot.add_cog(ServerInfo(bot))
