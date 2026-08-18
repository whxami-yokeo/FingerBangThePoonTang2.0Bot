import asyncio
import sys

import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
from mysql.connector import DatabaseError
from print_color import print
import os

from Bot import Bot
from utils.custom.errors.FingerBangThePoonTangBotError import FingerBangThePoonTangBotError, ConnectionUnsuccessful

load_dotenv()

if __name__ == "__main__":
    intents = discord.Intents.all()
    intents.voice_states = True
    bot = Bot(command_prefix=".", intents_=intents, token=os.getenv('DISCORD_TOKEN'))

    try:
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'discord.log')
        bot.run(token=bot.token, log_handler=logging.FileHandler(filename=log_path, encoding='utf-8', mode='w'), log_level=logging.INFO, reconnect=True)
    except DatabaseError as e:
        print(e, tag="CRITICAL", tag_color="red", color="white")
    finally:
        if bot.user:
            print(f"{bot.user.name} has been terminated!", tag="TERMINATED", tag_color="red", color="magenta", format="blink")
