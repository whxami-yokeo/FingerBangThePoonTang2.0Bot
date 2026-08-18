import discord
from discord import Color
from discord.ext import commands
import wikipedia
from discord.utils import utcnow


class WikipediaCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="wiki", help="Searches Wikipedia for the selected topic!")
    async def wiki(self, ctx: discord.ext.commands.Context, *, search_query: str = commands.Parameter(name="search_query", description="The page/article you would like to search Wikipedia for", kind=commands.Parameter.POSITIONAL_OR_KEYWORD)):

        if search_query is None:
            raise commands.MissingRequiredArgument(param=commands.Parameter('search_query', commands.Parameter.POSITIONAL_OR_KEYWORD, description="The page/article you would like to search Wikipedia for."))

        try:
            wikipedia.set_lang("en")
            summary = wikipedia.summary(search_query, sentences=2)
            page = wikipedia.page(search_query)
            url = page.url

            embed = discord.Embed(title=f"{search_query} has returned a result!", url=url, description=summary, colour=Color.blurple(), timestamp=utcnow()).set_footer(text=f"This message was brought to you by {self.bot.user.name}'s Message Delivery System!", icon_url=self.bot.user.avatar.url)
            await ctx.reply(embed=embed, mention_author=False)
        except wikipedia.exceptions.PageError:
            embed = EmbedGenerator(self.bot).generate_title_message_embed_with_footer(title="📛 An Error Has Occurred 📛", description=f"Could not find a Wikipedia page for {search_query}", colour=Color.red(), timestamp=True)
            await ctx.reply(embed=embed)
        except wikipedia.exceptions.DisambiguationError as e:
            embed = EmbedGenerator(self.bot).generate_title_message_embed_with_footer(title="📛 An Error Has Occurred 📛", description=f"Multiple results for {search_query}. Please be more specific. Options: {', '.join(e.options[:5])}...", colour=Color.red(), timestamp=True)
            await ctx.reply(embed=embed)
        except Exception as er:
            embed = EmbedGenerator(self.bot).generate_title_message_embed_with_footer(title="📛 An Error Has Occurred 📛", description=er, colour=Color.red(), timestamp=True)
            await ctx.reply(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(WikipediaCommands(bot))
