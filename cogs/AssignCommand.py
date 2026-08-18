import discord
from discord import Color
from discord.ext import commands

from utils.EmbedGeneratorUtil import EmbedGenerator
from utils.custom.errors.FingerBangThePoonTangBotError import RoleNotFoundError, AlreadyHasRoleError


class AssignCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(name="assign", help="Assigns The Role Of 'Member' To Users Who Initiate This Command.")
    async def assign(self, ctx: discord.ext.commands.Context):
        """
        Assigns the role of 'Member' to users who initiate this command
        :param ctx: This is the discord Interaction we can access data from.
        :return:
        """

        member_role = discord.utils.get(ctx.guild.roles, name="Member")

        if member_role is None:
            raise RoleNotFoundError(error="Incorrect name or role does not exist.")

        if member_role in ctx.author.roles:
            raise AlreadyHasRoleError(error="You Cannot Add This Role Again!")

        await ctx.author.add_roles(member_role)
        embed = EmbedGenerator(self.bot).generate_simple_message_embed(description=f"Successfully Added Role 'Member' To {ctx.author.mention}!", colour=Color.green())
        await ctx.reply(embed=embed, mention_author=False)


async def setup(bot: commands.Bot):
    await bot.add_cog(AssignCommand(bot))
