import discord
from discord import Color
from discord.ext import commands

from utils.EmbedGeneratorUtil import EmbedGenerator


class UnassignCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.has_role("Member")
    @commands.command(name="unassign", help="Unassigns the role of 'Member' from the user who initiate this command")
    async def unassign(self, ctx: discord.ext.commands.Context):
        """
        Unassigns the role of 'Member' from the user who initiate this command
        :param ctx: This is the discord Interaction we can access data from.
        :return:
        """

        member_role = discord.utils.get(ctx.guild.roles, name="Member") or None

        if member_role is None:
            embed = EmbedGenerator(self.bot).generate_simple_message_embed(description="There is no role with that name!", colour=Color.dark_orange(), timestamp=False)
            await ctx.reply(embed=embed, mention_author=False)
            raise commands.RoleNotFound(argument="The role 'Member' is not found in this guild!")

        await ctx.author.remove_roles(member_role)
        embed = EmbedGenerator(self.bot).generate_simple_message_embed(description=f"TSuccessfully removed role 'Member' from {ctx.author.display_name}!", colour=Color.green(), timestamp=False)
        await ctx.reply(embed=embed, mention_author=False)


async def setup(bot: commands.Bot):
    await bot.add_cog(UnassignCommand(bot))
