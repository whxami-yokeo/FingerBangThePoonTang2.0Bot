import discord
from discord import Color
from discord.ext import commands

from utils.EmbedGeneratorUtil import EmbedGenerator
from utils.custom.errors.FingerBangThePoonTangBotError import ChannelNotSupported
from utils.custom.views.TicketLauncherView import TicketLauncher


class TicketCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command(name="sendticketembed", help="Sends an embed with information about creating a ticket.")
    async def sendticketembed(self, ctx: commands.Context):
        await ctx.message.delete()
        embed_1 = EmbedGenerator(self.bot).generate_title_message_embed_with_footer(title="Ticket Support System", description="If you need support, click the button below to create a ticket!", colour=Color.magenta(), timestamp=True)

        await ctx.channel.send(embed=embed_1, view=TicketLauncher(self.bot))

    @commands.command(name="addmember", help="Adds a member to the current ticket channel!")
    async def addmember(self, ctx: commands.Context, user: discord.Member):
        if not isinstance(ctx.channel, discord.TextChannel):
            raise ChannelNotSupported(error="This command can only be ran in a text channel!")

        if ctx.author.name not in ctx.channel.name:
            if ctx.author.get_role(discord.utils.get(ctx.author.roles, name="Admin").id) is None:
                raise commands.MissingPermissions("You are not the owner of this ticket channel or an admin, you cannot add a member.")

        await ctx.channel.set_permissions(read_messages=True, send_messages=True, target=user)
        embed = EmbedGenerator.generate_simple_message_embed(description=f"{user.mention} has been added to this ticket channel!", colour=Color.green(), timestamp=False)
        await ctx.reply(embed=embed, mention_author=False)


async def setup(bot: commands.Bot):
    await bot.add_cog(TicketCommands(bot))
