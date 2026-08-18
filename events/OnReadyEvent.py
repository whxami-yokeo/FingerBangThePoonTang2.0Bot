import logging

import discord
from discord.ext import commands, tasks
import os
from print_color import print
from utils.custom.errors.FingerBangThePoonTangBotError import ChannelNotFound


class OnReady(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.start_log_loop.start()
        self.last_read_position = 0
        self.logger = logging.getLogger('discord')

    def cog_unload(self):
        self.start_log_loop.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Runs whenever the bot is started up and ready to run commands/events!
        :return:
        """

        for guild in self.bot.guilds:
            id = guild.id
            self.bot.musicQueue[id] = []
            self.bot.queueIndex[id] = 0
            self.bot.vc[id] = None
            self.bot.is_paused[id] = self.bot.is_playing[id] = False

        if not self.start_log_loop.is_running():
            self.start_log_loop.start()
        print(f"Successfully logged in as {self.bot.user.name}", tag="SUCCESS", tag_color="green", color="white")

        # log_channels = []
        # for guild in bot.guilds:
        #     log_channels.append(discord.utils.get(guild.channels, name="discord-log"))

    @tasks.loop(reconnect=True, seconds=1)
    async def start_log_loop(self):
        try:
            found_channel = None

            for guild in self.bot.guilds:
                if guild.name == 'Bot Testing Server 2':
                    channel = discord.utils.get(guild.channels, name='discord-log')
                    if channel is not None:
                        found_channel = channel
                    else:
                        category = discord.utils.get(guild.categories, name='logs')

                        if category:
                            new_channel_position = len(category.channels)

                            try:
                                found_channel = await guild.create_text_channel('discord-log', category=category,
                                                                                position=new_channel_position)
                                log_ = print(f'{found_channel.name} text channel!', tag="CREATED", tag_color="green",
                                             color="white")
                                self.logger.info(msg=log_)
                            except Exception as e:
                                print('start_log_loop', e)

            log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'discord.log')

            if not os.path.exists(log_path):
                print(f"Log file not found at {log_path}")
                raise FileNotFoundError(
                    f"Log file not found at {log_path}")

            with open(log_path, 'r', encoding='utf-8') as f:
                f.seek(self.last_read_position)
                new_content = f.read()
                self.last_read_position = f.tell()

                if new_content:
                    # Split content into chunks if it's too long for a single message
                    for chunk in [new_content[i:i + 2000] for i in range(0, len(new_content), 2000)]:
                        await found_channel.send(f"```\n{chunk}\n```")  # Send as a code block for formatting
        except Exception as e:
            print(f"An error occurred: {e}")

    @start_log_loop.before_loop
    async def before_log_loop(self):
        print('\nLogging in...')
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(OnReady(bot))
