import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bot.events import setup_events

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='suckme', intents=intents)

setup_events(bot)

bot.run(os.getenv('TOKEN'))